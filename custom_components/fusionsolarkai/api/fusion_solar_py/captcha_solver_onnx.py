"""Captcha solver for the FusionSolar login flow.

This file sends captcha images to a third-party Hugging Face Space
(Nischay103/captcha_recognition) for recognition. That Space is NOT
controlled by this project; its availability and behaviour can change
without notice.

The filename `captcha_solver_onnx.py` is historical -- earlier versions
used local ONNX inference. The current implementation delegates to the
remote Gradio API instead.
"""

import time
import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

from .exceptions import FusionSolarException, FusionSolarRateLimit

_LOGGER = logging.getLogger(__name__)

_GRADIO_TIMEOUT = 30  # seconds – total budget for Client() + predict()


def _run_with_timeout(func, timeout_seconds=_GRADIO_TIMEOUT):
    """Run *func* in a separate thread with a hard timeout.

    This replaces the old signal.SIGALRM approach which only works in the
    main thread.  Home Assistant calls us from a thread-pool worker, so
    we need a threading-safe timeout mechanism.
    """
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func)
        try:
            return future.result(timeout=timeout_seconds)
        except FuturesTimeoutError:
            raise FusionSolarException(
                f"Captcha solving timed out after {timeout_seconds} seconds"
            )


class Solver(object):
    def __init__(self, hass):
        self.hass = hass
        self.last_rate_limit = 0

    RATE_LIMIT_COOLDOWN = 6 * 60 * 60  # 6-hour cooldown

    def solve_captcha_rest(self, img_bytes: bytes) -> str:
        """Send captcha image bytes to Nischay103/captcha_recognition via gradio_client."""
        try:
            from gradio_client import Client, handle_file
        except ImportError:
            raise FusionSolarException(
                "gradio_client is not installed. Run: pip install gradio_client"
            )

        import tempfile
        import os

        tmp_path = None

        # Write bytes to a temp file since handle_file expects a path or URL
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp.write(img_bytes)
            tmp_path = tmp.name

        try:
            _LOGGER.debug(
                "Sending captcha image (%d bytes) to Hugging Face Space for solving",
                len(img_bytes),
            )

            def _do_predict():
                client = Client("Nischay103/captcha_recognition")
                return client.predict(
                    input=handle_file(tmp_path),
                    api_name="/predict",
                )

            result = _run_with_timeout(_do_predict)

            # Validate the response
            if not isinstance(result, str) or not result.strip():
                _LOGGER.warning(
                    "Captcha Gradio API returned an invalid response: %r", result
                )
                raise FusionSolarException(
                    f"Captcha API returned an invalid or empty response: {result!r}"
                )

            _LOGGER.debug("Captcha solved: %s", result)
            return str(result).strip().upper()
        except FusionSolarException:
            raise
        except Exception as exc:
            _LOGGER.warning("External captcha service failed: %s", exc)
            raise
        finally:
            if tmp_path is not None:
                os.remove(tmp_path)

    def solve_captcha(self, img_bytes: bytes) -> str:
        if time.time() - self.last_rate_limit < self.RATE_LIMIT_COOLDOWN:
            raise FusionSolarRateLimit(
                "Captcha solving temporarily disabled due to rate limiting. Try again later."
            )

        try:
            return self.solve_captcha_rest(img_bytes)
        except FusionSolarRateLimit:
            raise
        except Exception as e:
            _LOGGER.error("Captcha solving failed: %s", e)
            self.last_rate_limit = time.time()
            raise FusionSolarRateLimit(
                f"Captcha API failed, please try again in 6 hours: {e}"
            )
