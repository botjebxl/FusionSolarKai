# FusionSolarKai

A security-focused Home Assistant integration for Huawei FusionSolar systems. Monitor your solar plant, inverters, batteries, power sensors, chargers, and more — directly from the FusionSolar cloud API. No northbound API, OpenAPI, or kiosk URL required.

> **Credit**: Originally based on [FusionSolarPlus](https://github.com/JortvanSchijndel/FusionSolarPlus) by [@JortvanSchijndel](https://github.com/JortvanSchijndel). FusionSolarKai has since been independently developed with a focus on security hardening, improved error handling, and additional features.

___

## What's different?

- Hardened authentication flow (SSRF protection, encryption downgrade prevention, redirect validation)
- Proper error surfacing to Home Assistant (reauth prompts, retry-on-failure, no silent swallowing)
- Alarm monitoring via binary sensors on every device
- Configurable polling interval (15–300 seconds)
- Pinned dependencies and supply chain improvements
- All entities created on startup regardless of time of day

## Setup

<a href="https://my.home-assistant.io/redirect/hacs_repository/?owner=botjebxl&repository=FusionSolarKai&category=Integration" target="_blank" rel="noreferrer noopener"><img src="https://my.home-assistant.io/badges/hacs_repository.svg" alt="Open your Home Assistant instance and open a repository inside the Home Assistant Community Store." /></a>

Or add manually in HACS: **Custom repositories** → `botjebxl/FusionSolarKai` → Category: Integration.

Once installed:

1. Restart Home Assistant and go to **Settings → Devices & Services**
2. Click **Add Integration**
3. Search for **"FusionSolarKai"**
4. Enter your FusionSolar username, password, and subdomain
5. Select the device type you want to add, then choose the specific device

Repeat steps 2–5 for each device you want to monitor.

# Energy Dashboard

FusionSolarKai is fully compatible with the Home Assistant energy dashboard. Make sure you’ve added the relevant device types first (see setup steps above).

When configuring the energy dashboard you need to provide the following settings:

|                          | Energy dashboard setting         | Device Type  | Entity                           |
|--------------------------|----------------------------------|:------------:|----------------------------------|
| **Electricity Grid**     | Grid Consumption                 | Power Sensor | Negative Active Energy           |
|                          | Return to Grid                   | Power Sensor | Positive Active Energy           |
| **Home Battery Storage** | Energy going in to the battery   |   Battery    | Energy Charged Today             |
|                          | Energy coming out of the battery |   Battery    | Energy Discharged Today          |
| **Solar Panels**         | Solar Production                 |   Inverter   | Daily Energy (for each inverter) |
# Entities


<details>
<summary>Click here to see the list of entities </summary>

<details>
<summary><b><ins>Inverter</ins></b></summary>

<p><b>Inverter Signals</b></p>
<table>
   <tr>
      <td align="center"><b>#</b></td>
      <td><b>Entity Display Name</b></td>
      <td align="center"><b>Unit</b></td>
   </tr>
   <tr>
      <td align="center">1</td>
      <td>Status</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">2</td>
      <td>Power Factor</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">3</td>
      <td>Output Mode</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">4</td>
      <td>Last Startup Time</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">5</td>
      <td>Last Shutdown Time</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">6</td>
      <td>Daily Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">7</td>
      <td>Total Energy Produced</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">8</td>
      <td>Current Active Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">9</td>
      <td>Reactive Power</td>
      <td align="center">kvar</td>
   </tr>
   <tr>
      <td align="center">10</td>
      <td>Rated Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">11</td>
      <td>Grid Frequency</td>
      <td align="center">Hz</td>
   </tr>
   <tr>
      <td align="center">12</td>
      <td>Phase A Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">13</td>
      <td>Phase B Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">14</td>
      <td>Phase C Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">15</td>
      <td>Phase A Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">16</td>
      <td>Phase B Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">17</td>
      <td>Phase C Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">18</td>
      <td>Temperature</td>
      <td align="center">°C</td>
   </tr>
   <tr>
      <td align="center">19</td>
      <td>Insulation Resistance</td>
      <td align="center">MΩ</td>
   </tr>
</table>

<p><b>PV Signals</b></p>
<table>
   <tr>
      <td align="center"><b>#</b></td>
      <td><b>Entity Display Name</b></td>
      <td align="center"><b>Unit</b></td>
   </tr>
   <tr>
      <td align="center">1</td>
      <td>[PV 1] Input Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">2</td>
      <td>[PV 1] Input Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">3</td>
      <td>[PV 1] Input Power</td>
      <td align="center">W</td>
   </tr>
</table>
<p><i>* [PV 1] can be [PV 1] to [PV 20] depending on your device.</i></p>

<p><b>Optimizer Metrics</b></p>
<table>
   <tr>
      <td align="center"><b>#</b></td>
      <td><b>Entity Display Name</b></td>
      <td align="center"><b>Unit</b></td>
   </tr>
   <tr>
      <td align="center">1</td>
      <td>Output Power</td>
      <td align="center">W</td>
   </tr>
   <tr>
      <td align="center">2</td>
      <td>Total Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">3</td>
      <td>Input Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">4</td>
      <td>Running Status</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">5</td>
      <td>Temperature</td>
      <td align="center">°C</td>
   </tr>
   <tr>
      <td align="center">6</td>
      <td>SN</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">7</td>
      <td>Optimizer Number</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">8</td>
      <td>Output Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">9</td>
      <td>Input Current</td>
      <td align="center">A</td>
   </tr>
</table>
</details>

<details>
<summary><b><ins>Battery</ins></b></summary>

<p><b>Battery Status Signals</b></p>
<table>
   <tr>
      <td align="center"><b>#</b></td>
      <td><b>Entity Display Name</b></td>
      <td align="center"><b>Unit</b></td>
   </tr>
   <tr>
      <td align="center">1</td>
      <td>Operating Status</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">2</td>
      <td>Charge/Discharge Mode</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">3</td>
      <td>Rated Capacity</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">4</td>
      <td>Backup Time</td>
      <td align="center">min</td>
   </tr>
   <tr>
      <td align="center">5</td>
      <td>Energy Charged Today</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">6</td>
      <td>Energy Discharged Today</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">7</td>
      <td>Charge/Discharge Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">8</td>
      <td>Bus Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">9</td>
      <td>State of Charge</td>
      <td align="center">%</td>
   </tr>
</table>

<p><b>Battery Module Signals</b></p>
<table>
   <tr>
      <td align="center"><b>#</b></td>
      <td><b>Entity Display Name</b></td>
      <td align="center"><b>Unit</b></td>
   </tr>
   <tr>
      <td align="center">1</td>
      <td>[Module 1] No.</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">2</td>
      <td>[Module 1] Working Status</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">3</td>
      <td>[Module 1] SN</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">4</td>
      <td>[Module 1] Software Version</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">5</td>
      <td>[Module 1] SOC</td>
      <td align="center">%</td>
   </tr>
   <tr>
      <td align="center">6</td>
      <td>[Module 1] Charge and Discharge Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">7</td>
      <td>[Module 1] Internal Temperature</td>
      <td align="center">°C</td>
   </tr>
   <tr>
      <td align="center">8</td>
      <td>[Module 1] Daily Charge Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">9</td>
      <td>[Module 1] Daily Discharge Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">10</td>
      <td>[Module 1] Total Discharge Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">11</td>
      <td>[Module 1] Bus Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">12</td>
      <td>[Module 1] Bus Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">13</td>
      <td>[Module 1] FE Connection</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">14</td>
      <td>[Module 1] Total Charge Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">15</td>
      <td>[Module 1] Battery Pack 1 No.</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">16</td>
      <td>[Module 1] Battery Pack 2 No.</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">17</td>
      <td>[Module 1] Battery Pack 3 No.</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">18</td>
      <td>[Module 1] Battery Pack 1 Firmware Version</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">19</td>
      <td>[Module 1] Battery Pack 2 Firmware Version</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">20</td>
      <td>[Module 1] Battery Pack 3 Firmware Version</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">21</td>
      <td>[Module 1] Battery Pack 1 SN</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">22</td>
      <td>[Module 1] Battery Pack 2 SN</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">23</td>
      <td>[Module 1] Battery Pack 3 SN</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">24</td>
      <td>[Module 1] Battery Pack 1 Operating Status</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">25</td>
      <td>[Module 1] Battery Pack 2 Operating Status</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">26</td>
      <td>[Module 1] Battery Pack 3 Operating Status</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">27</td>
      <td>[Module 1] Battery Pack 1 Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">28</td>
      <td>[Module 1] Battery Pack 2 Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">29</td>
      <td>[Module 1] Battery Pack 3 Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">30</td>
      <td>[Module 1] Battery Pack 1 Charge/Discharge Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">31</td>
      <td>[Module 1] Battery Pack 2 Charge/Discharge Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">32</td>
      <td>[Module 1] Battery Pack 3 Charge/Discharge Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">33</td>
      <td>[Module 1] Battery Pack 1 Maximum Temperature</td>
      <td align="center">°C</td>
   </tr>
   <tr>
      <td align="center">34</td>
      <td>[Module 1] Battery Pack 2 Maximum Temperature</td>
      <td align="center">°C</td>
   </tr>
   <tr>
      <td align="center">35</td>
      <td>[Module 1] Battery Pack 3 Maximum Temperature</td>
      <td align="center">°C</td>
   </tr>
   <tr>
      <td align="center">36</td>
      <td>[Module 1] Battery Pack 1 Minimum Temperature</td>
      <td align="center">°C</td>
   </tr>
   <tr>
      <td align="center">37</td>
      <td>[Module 1] Battery Pack 2 Minimum Temperature</td>
      <td align="center">°C</td>
   </tr>
   <tr>
      <td align="center">38</td>
      <td>[Module 1] Battery Pack 3 Minimum Temperature</td>
      <td align="center">°C</td>
   </tr>
   <tr>
      <td align="center">39</td>
      <td>[Module 1] Battery Pack 1 SOC</td>
      <td align="center">%</td>
   </tr>
   <tr>
      <td align="center">40</td>
      <td>[Module 1] Battery Pack 2 SOC</td>
      <td align="center">%</td>
   </tr>
   <tr>
      <td align="center">41</td>
      <td>[Module 1] Battery Pack 3 SOC</td>
      <td align="center">%</td>
   </tr>
   <tr>
      <td align="center">42</td>
      <td>[Module 1] Battery Pack 1 Total Discharge Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">43</td>
      <td>[Module 1] Battery Pack 2 Total Discharge Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">44</td>
      <td>[Module 1] Battery Pack 3 Total Discharge Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">45</td>
      <td>[Module 1] Battery Pack 1 Battery Health Check</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">46</td>
      <td>[Module 1] Battery Pack 2 Battery Health Check</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">47</td>
      <td>[Module 1] Battery Pack 3 Battery Health Check</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">48</td>
      <td>[Module 1] Battery Pack 1 Heating Status</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">49</td>
      <td>[Module 1] Battery Pack 2 Heating Status</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">50</td>
      <td>[Module 1] Battery Pack 3 Heating Status</td>
      <td align="center"></td>
   </tr>
</table>
<p><i>* [Module 1] can be [Module 1] to [Module 4] depending on your device.</i></p>
</details>

<details>
<summary><b><ins>Power Sensor</ins></b></summary>

<p><b>Power Sensor Signals</b></p>
<table>
   <tr>
      <td align="center"><b>#</b></td>
      <td><b>Entity Display Name</b></td>
      <td align="center"><b>Unit</b></td>
   </tr>
   <tr>
      <td align="center">1</td>
      <td>Meter Status</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">2</td>
      <td>Positive Active Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">3</td>
      <td>Negative Active Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">4</td>
      <td>Reactive Power</td>
      <td align="center">var</td>
   </tr>
   <tr>
      <td align="center">5</td>
      <td>Active Power</td>
      <td align="center">W</td>
   </tr>
   <tr>
      <td align="center">6</td>
      <td>Power Factor</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">7</td>
      <td>Phase A Active Power</td>
      <td align="center">W</td>
   </tr>
   <tr>
      <td align="center">8</td>
      <td>Phase B Active Power</td>
      <td align="center">W</td>
   </tr>
   <tr>
      <td align="center">9</td>
      <td>Phase C Active Power</td>
      <td align="center">W</td>
   </tr>
   <tr>
      <td align="center">10</td>
      <td>Phase A Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">11</td>
      <td>Phase B Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">12</td>
      <td>Phase C Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">13</td>
      <td>Phase A Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">14</td>
      <td>Phase B Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">15</td>
      <td>Phase C Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">16</td>
      <td>Grid Frequency</td>
      <td align="center">Hz</td>
   </tr>
</table>

<p><b>Emma A02 Signals</b></p>
<table>
   <tr>
      <td align="center"><b>#</b></td>
      <td><b>Entity Display Name</b></td>
      <td align="center"><b>Unit</b></td>
   </tr>
   <tr>
      <td align="center">1</td>
      <td>Forward Active Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">2</td>
      <td>Reverse Active Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">3</td>
      <td>Reactive Power</td>
      <td align="center">kvar</td>
   </tr>
   <tr>
      <td align="center">4</td>
      <td>Active Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">5</td>
      <td>Power Factor</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">6</td>
      <td>Phase A Active Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">7</td>
      <td>Phase B Active Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">8</td>
      <td>Phase C Active Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">9</td>
      <td>Phase A Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">10</td>
      <td>Phase B Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">11</td>
      <td>Phase C Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">12</td>
      <td>Phase A Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">13</td>
      <td>Phase B Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">14</td>
      <td>Phase C Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">15</td>
      <td>RS485-2 Port Mode</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">16</td>
      <td>WiFi Signal Strength</td>
      <td align="center">dBm</td>
   </tr>
   <tr>
      <td align="center">17</td>
      <td>Signal Strength</td>
      <td align="center">dBm</td>
   </tr>
</table>

<p><b>DTSU666-FE Signals</b></p>
<table>
   <tr>
      <td align="center"><b>#</b></td>
      <td><b>Entity Display Name</b></td>
      <td align="center"><b>Unit</b></td>
   </tr>
   <tr>
      <td align="center">1</td>
      <td>Communication Status</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">2</td>
      <td>AB Line Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">3</td>
      <td>BC Line Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">4</td>
      <td>CA Line Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">5</td>
      <td>Phase A Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">6</td>
      <td>Phase B Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">7</td>
      <td>Phase C Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">8</td>
      <td>Phase A Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">9</td>
      <td>Phase B Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">10</td>
      <td>Phase C Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">11</td>
      <td>Active Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">12</td>
      <td>Reactive Power</td>
      <td align="center">kVar</td>
   </tr>
   <tr>
      <td align="center">13</td>
      <td>Power Factor</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">14</td>
      <td>Phase A Active Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">15</td>
      <td>Phase B Active Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">16</td>
      <td>Phase C Active Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">17</td>
      <td>iAcMeter</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">18</td>
      <td>iAcMeter IP</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">19</td>
      <td>Comm Status</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">20</td>
      <td>iAcMeter Mode</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">21</td>
      <td>Meter Data Source</td>
      <td align="center"></td>
   </tr>
</table>
</details>

<details>
<summary><b><ins>Charger</ins></b></summary>

<p><b>Charging Pile Signals</b></p>
<table>
   <tr>
      <td align="center"><b>#</b></td>
      <td><b>Entity Display Name</b></td>
      <td align="center"><b>Unit</b></td>
   </tr>
   <tr>
      <td align="center">1</td>
      <td>Connector Number</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">2</td>
      <td>Connector Type</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">3</td>
      <td>Rated Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">4</td>
      <td>Status</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">5</td>
      <td>Relay Status</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">6</td>
      <td>Connector Temp</td>
      <td align="center">°C</td>
   </tr>
   <tr>
      <td align="center">7</td>
      <td>Phase A Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">8</td>
      <td>Phase C Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">9</td>
      <td>Phase B Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">10</td>
      <td>Output Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">11</td>
      <td>PWM Duty</td>
      <td align="center">%</td>
   </tr>
   <tr>
      <td align="center">12</td>
      <td>Connector Lock</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">13</td>
      <td>Working Mode</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">14</td>
      <td>Departure Time</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">15</td>
      <td>Planned Charge Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">16</td>
      <td>Connection Status</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">17</td>
      <td>Charging Duration</td>
      <td align="center">s</td>
   </tr>
</table>

<p><b>Charger Device Signals</b></p>
<table>
   <tr>
      <td align="center"><b>#</b></td>
      <td><b>Entity Display Name</b></td>
      <td align="center"><b>Unit</b></td>
   </tr>
   <tr>
      <td align="center">1</td>
      <td>FW Version</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">2</td>
      <td>HW Version</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">3</td>
      <td>Serial Number</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">4</td>
      <td>Rated Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">5</td>
      <td>Phase A Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">6</td>
      <td>Phase B Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">7</td>
      <td>Phase C Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">8</td>
      <td>Model</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">9</td>
      <td>Total Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">10</td>
      <td>Charger Temp</td>
      <td align="center">°C</td>
   </tr>
   <tr>
      <td align="center">11</td>
      <td>Port Count</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">12</td>
      <td>Bluetooth Name</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">13</td>
      <td>Device Status</td>
      <td align="center"></td>
   </tr>
</table>
</details>

<details>
<summary><b><ins>Plant</ins></b></summary>

<p><b>Plant Signals</b></p>
<table>
   <tr>
      <td align="center"><b>#</b></td>
      <td><b>Entity Display Name</b></td>
      <td align="center"><b>Unit</b></td>
   </tr>
   <tr>
      <td align="center">1</td>
      <td>Monthly Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">2</td>
      <td>Total Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">3</td>
      <td>Today Income</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">4</td>
      <td>Today Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">5</td>
      <td>Yearly Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">6</td>
      <td>Self Used Energy Today</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">7</td>
      <td>Consumption Today</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">8</td>
      <td>PV Self Consumption</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">9</td>
      <td>PV Feed-In Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">10</td>
      <td>Imported Grid Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">11</td>
      <td>Total Consumption</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">12</td>
      <td>Grid Import Ratio</td>
      <td align="center">%</td>
   </tr>
   <tr>
      <td align="center">13</td>
      <td>Self Consumption Ratio</td>
      <td align="center">%</td>
   </tr>
   <tr>
      <td align="center">14</td>
      <td>Self Consumption Ratio (by PV production)</td>
      <td align="center">%</td>
   </tr>
   <tr>
      <td align="center">15</td>
      <td>Flow Solar Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">16</td>
      <td>Flow Battery Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">17</td>
      <td>Flow Load Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">18</td>
      <td>Flow Buy Power</td>
      <td align="center">kW</td>
   </tr>
</table>
</details>

<details>
<summary><b><ins>BackupBox</ins></b></summary>

<p><b>BackupBox Signals</b></p>
<table>
   <tr>
      <td align="center"><b>#</b></td>
      <td><b>Entity Display Name</b></td>
      <td align="center"><b>Unit</b></td>
   </tr>
   <tr>
      <td align="center">1</td>
      <td>Status</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">2</td>
      <td>Grid A Phase Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">3</td>
      <td>Grid B Phase Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">4</td>
      <td>Grid C Phase Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">5</td>
      <td>Phase A Voltage of Backup Load</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">6</td>
      <td>Phase B Voltage of Backup Load</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">7</td>
      <td>Phase C Voltage of Backup Load</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">8</td>
      <td>Internal Ambient Temperature</td>
      <td align="center">°C</td>
   </tr>
</table>
</details>

<details>
<summary><b><ins>EMMA</ins></b></summary>

<p><b>EMMA Signals</b></p>
<table>
   <tr>
      <td align="center"><b>#</b></td>
      <td><b>Entity Display Name</b></td>
      <td align="center"><b>Unit</b></td>
   </tr>
   <tr>
      <td align="center">1</td>
      <td>Forward Active Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">2</td>
      <td>Reverse Active Energy</td>
      <td align="center">kWh</td>
   </tr>
   <tr>
      <td align="center">3</td>
      <td>Reactive Power</td>
      <td align="center">kvar</td>
   </tr>
   <tr>
      <td align="center">4</td>
      <td>Active Power</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">5</td>
      <td>Power Factor</td>
      <td align="center"></td>
   </tr>
   <tr>
      <td align="center">6</td>
      <td>Active Power Pa</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">7</td>
      <td>Active Power Pb</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">8</td>
      <td>Active Power Pc</td>
      <td align="center">kW</td>
   </tr>
   <tr>
      <td align="center">9</td>
      <td>Phase A Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">10</td>
      <td>Phase B Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">11</td>
      <td>Phase C Voltage</td>
      <td align="center">V</td>
   </tr>
   <tr>
      <td align="center">12</td>
      <td>Phase A Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">13</td>
      <td>Phase B Current</td>
      <td align="center">A</td>
   </tr>
   <tr>
      <td align="center">14</td>
      <td>Phase C Current</td>
      <td align="center">A</td>
   </tr>
</table>
</details>

</details>

# Issues
If you encounter any problems, please [open an issue](https://github.com/botjebxl/FusionSolarKai/issues) with as much detail as possible.

# Development

To contribute or run FusionSolarKai locally:

1. **Install VS Code:**  
   [Download and install Visual Studio Code](https://code.visualstudio.com/).

2. **Install Docker:**  
   [Download and install Docker](https://docs.docker.com/get-docker/).

3. **Clone the repository:**
   ```bash
   git clone https://github.com/botjebxl/FusionSolarKai.git && cd FusionSolarKai
   ```

4. **Copy the dev container configuration:**
   ```bash
   cp .devcontainer/devcontainer.json.sample .devcontainer/devcontainer.json
   ```

5. **Open the project in VS Code:**
   ```bash
   code .
   ```

6. **Start the development container:**
   - Open the Command Palette (Mac: `Cmd+Shift+P`, Windows/Linux: `Ctrl+Shift+P`)
   - Type `Dev Containers: Rebuild and Reopen in Container` and press Enter.

This will set up a reproducible development environment with all dependencies installed and Home Assistant will be accessible at http://localhost:8123.

# Legal Notice
This integration for Home Assistant uses a custom modified version of [FusionSolarPy](https://github.com/jgriss/FusionSolarPy).


