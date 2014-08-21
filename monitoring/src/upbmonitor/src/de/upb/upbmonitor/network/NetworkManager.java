package de.upb.upbmonitor.network;

import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.util.ArrayList;

import de.upb.upbmonitor.R;
import android.util.Log;
import de.upb.upbmonitor.commandline.Shell;
import de.upb.upbmonitor.monitoring.model.UeContext;

public class NetworkManager
{
	private static final String LTAG = "NetworkManager";
	// this is maybe vendor specific (tested on Samsung Galaxy Nexsus):
	private static final String WIFI_INTERFACE = "wlan0";
	private static final String MOBILE_INTERFACE = "rmnet0";
	private static NetworkManager INSTANCE;

	public static String WPA_TEMPLATE = null;

	/**
	 * Use as singleton class.
	 * 
	 * @return class instance
	 */
	public synchronized static NetworkManager getInstance()
	{
		if (INSTANCE == null)
			INSTANCE = new NetworkManager();
		return INSTANCE;
	}

	public synchronized void enableDualNetworking()
	{
		// TODO: Split so that WiFi reconnection is easily possible!

		// create a individual configuration for wpa_supplicant
		// setWifiConfiguration("peuroam", "meinwaldecklebehoch");
		setWifiConfiguration("peu-test", null);

		Log.i(LTAG, "Enabling dual networking");
		// stop dhcp client
		Shell.execute("pkill dhcpcd");
		// kill wifi management
		Shell.execute("pkill wpa_supplicant");
		// disable wifi with the wifi manager
		Shell.execute("svc wifi disable");
		// enable mobile with mobile manager
		Shell.execute("svc data enable");
		// bring up wifi interface by hand
		Shell.execute("netcfg wlan0 up");
		// configure target wifi (copy indiv. config to destination)
		Shell.execute("cp /sdcard/wpa_supplicant.conf /data/misc/wifi/wpa_supplicant.conf");
		Shell.execute("chmod 666 /data/misc/wifi/wpa_supplicant.conf");
		// connect to actual wifi
		Shell.execute("wpa_supplicant -B -Dnl80211 -iwlan0 -c/data/misc/wifi/wpa_supplicant.conf");
		// bring up dhcp client and receive ip (takes some time!)
		Shell.execute("dhcpcd wlan0");

	}

	public synchronized void disableDualNetworking()
	{
		Log.i(LTAG, "Disabling dual networking");
		// kill dhcp client
		Shell.execute("pkill dhcpcd");
		// kill wifi management
		Shell.execute("pkill wpa_supplicant");
		// tear down wifi interface
		Shell.execute("netcfg wlan0 down");
		// disable wifi in manager
		Shell.execute("svc wifi disable");
		// disable data in manager
		Shell.execute("svc data disable");
	}

	public synchronized boolean isDualNetworkingEnabled()
	{
		return (this.isMobileInterfaceEnabled() && this
				.isWiFiInterfaceEnabled());
	}

	public synchronized boolean isWiFiInterfaceEnabled()
	{
		return this.isInterfaceUp(WIFI_INTERFACE);
	}

	public synchronized boolean isMobileInterfaceEnabled()
	{
		return this.isInterfaceUp(MOBILE_INTERFACE);
	}

	/**
	 * ====================== HELPER ======================
	 */

	private synchronized boolean isInterfaceUp(String interfaceName)
	{
		ArrayList<String> status = this.getInterfaceStatus(interfaceName);
		// check result for errors
		if (status == null || status.size() < 2)
			return false;

		Log.d(LTAG,
				"Interface state of " + interfaceName + ": " + status.get(1));

		// check against state field
		if (status.get(1).equals("DOWN"))
			return false;
		return true;
	}

	/**
	 * Uses "netcfg" command to receive interface states, IPs, etc.
	 * 
	 * @param interfaceName
	 * @return ArrayList<String> containing (interface name, status, IP, ?, mac)
	 */
	private synchronized ArrayList<String> getInterfaceStatus(
			String interfaceName)
	{

		// execute netcfg command to check interface state
		ArrayList<String> out = Shell.executeBlocking("netcfg | grep "
				+ interfaceName);
		// if output is not one line, something went wrong
		if (out.size() < 1)
		{
			Log.e(LTAG, "Bad netcfg result.");
			return null;
		}
		// parse output and put all interesting values into array
		ArrayList<String> result = new ArrayList<String>();
		String l = out.get(out.size() - 1); // always use last line
		for (String p : l.split(" "))
			if (p.length() > 1)
				result.add(p);
		return result;
	}

	/**
	 * Writs the WiFi configuration to the wpa_supplicant.conf file. Needs the
	 * SSID of the target Wifi. WPA_PSK can be the WiFi's key, or null in order
	 * to use no encryption.
	 * 
	 * Resulting config file is written to SD-card and has to be copied from
	 * there, because we are not allowed to write into system files.
	 * 
	 * @param ssid
	 * @param wpa_psk
	 * @return
	 */
	private boolean setWifiConfiguration(String ssid, String wpa_psk)
	{
		// definitions
		String filename = "/sdcard/wpa_supplicant.conf";
		String config_str = WPA_TEMPLATE;
		String key_mgmt = wpa_psk == null ? "NONE" : "WPA-PSK";

		// set configuration values in teplate
		config_str = config_str.replace("${SSID}", ssid); // set ssid
		if (wpa_psk != null)
			config_str = config_str.replace("${WPA_PSK}", wpa_psk); // psk
		else
			config_str = config_str.replace("\tpsk=\"${WPA_PSK}\"\n", ""); // no
																			// psk
		config_str = config_str.replace("${KEY_MGMT}", key_mgmt); // mode

		// write configuration file to SD card (is copied later, since we are
		// not allowed to write system paths)
		try
		{
			FileOutputStream f = new FileOutputStream(filename);
			f.write(config_str.getBytes());
			f.close();
		} catch (Exception e)
		{
			e.printStackTrace();
			return false;
		}
		return true;
	}

}
