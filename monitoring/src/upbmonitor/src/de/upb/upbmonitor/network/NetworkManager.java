package de.upb.upbmonitor.network;

import java.util.ArrayList;

import android.util.Log;
import de.upb.upbmonitor.commandline.BlockingCommand;
import de.upb.upbmonitor.monitoring.model.UeContext;

public class NetworkManager
{
	private static final String LTAG = "NetworkManager";
	// this is maybe vendor specific (tested on Samsung Galaxy Nexsus):
	private static final String WIFI_INTERFACE = "wlan0";
	private static final String MOBILE_INTERFACE = "rmnet0";
	private static NetworkManager INSTANCE;

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
		Log.i(LTAG, "Enabling dual networking");
		// 1. stop dhcp client
		BlockingCommand.execute("pkill dhcpcd");
		// 2. disable wifi with the wifi manager
		BlockingCommand.execute("svc wifi disable");
		// 3. enable mobile with mobile manager
		BlockingCommand.execute("svc data enable");
		// 4. bring up wifi interface by hand
		BlockingCommand.execute("netcfg wlan0 up");
		// 5. configure target wifi
		// TODO conf target wifi
		// 6. connect to actual wifi
		BlockingCommand.execute("wpa_supplicant -B -Dnl80211 -iwlan0 -c/data/misc/wifi/wpa_supplicant.conf");
		// 7. bring up dhcp client and receive ip (takes some time!)
		BlockingCommand.execute("dhcpcd wlan0 &");	
	}

	public synchronized void disableDualNetworking()
	{
		Log.i(LTAG, "Disabling dual networking");
		// kill dhcp client
		BlockingCommand.execute("pkill dhcpcd");
		// kill wifi management
		BlockingCommand.execute("pkill wpa_supplicant");
		// tear down wifi interface
		BlockingCommand.execute("netcfg wlan0 down");
		// disable wifi in manager
		BlockingCommand.execute("svc wifi disable");
		// disable data in manager
		BlockingCommand.execute("svc data disable");
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
		ArrayList<String> out = BlockingCommand.execute("netcfg | grep "
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

}
