package de.upb.upbmonitor;

import java.util.ArrayList;

import com.stericson.RootTools.RootTools;

import de.upb.upbmonitor.monitoring.MonitoringService;
import de.upb.upbmonitor.network.NetworkManager;
import android.support.v4.app.Fragment;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CompoundButton;
import android.widget.Toast;
import android.widget.CompoundButton.OnCheckedChangeListener;
import android.widget.Switch;

public class ControlFragment extends Fragment
{
	private static final String LTAG = "ControlFragment";

	// singelton instance
	private static ControlFragment INSTANCE = null;

	private View rootView;
	private Switch switchMonitoringService;
	private Switch switchDualNetworking;

	/**
	 * Returns a new instance of this fragment for the given section number.
	 */
	public static ControlFragment getInstance()
	{
		if (INSTANCE == null)
			INSTANCE = new ControlFragment();
		return INSTANCE;
	}

	public ControlFragment()
	{

	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState)
	{
		this.rootView = inflater.inflate(R.layout.fragment_control, container,
				false);

		this.switchMonitoringService = (Switch) rootView
				.findViewById(R.id.switch_monitoringservice);
		this.switchDualNetworking = (Switch) rootView
				.findViewById(R.id.switch_dualnetworking);

		// set switch states based on service state
		this.switchMonitoringService
				.setChecked(MonitoringService.SERVICE_EXISTS);

		// monitoring switch listener
		this.switchMonitoringService
				.setOnCheckedChangeListener(new OnCheckedChangeListener()
				{

					@Override
					public void onCheckedChanged(CompoundButton buttonView,
							boolean isChecked)
					{
						if (isChecked)
							startMonitoringService();
						else
							stopMonitoringService();
					}
				});

		// dual networking listener
		this.switchDualNetworking
				.setOnCheckedChangeListener(new OnCheckedChangeListener()
				{

					@Override
					public void onCheckedChanged(CompoundButton buttonView,
							boolean isChecked)
					{
						if (isChecked)
							startDualNetworking();
						else
							stopDualNetworking();
					}
				});

		// check for root/busybox capabilities of device and disable
		// dual network switch if not available
		this.switchDualNetworking.setEnabled(this.checkRootAvailability()
				&& this.checkBusyBoxAvailability());

		return rootView;
	}

	public void startMonitoringService()
	{
		Intent i = new Intent(this.getActivity(), MonitoringService.class);
		this.getActivity().startService(i);
		// set switch state
		this.switchMonitoringService.setChecked(true);
		Log.i(LTAG, "Monitoring service turned on");
	}

	public void stopMonitoringService()
	{
		Intent i = new Intent(this.getActivity(), MonitoringService.class);
		this.getActivity().stopService(i);
		// set switch state
		this.switchMonitoringService.setChecked(false);
		Log.i(LTAG, "Monitoring service turned off");
	}

	public void startDualNetworking()
	{
		Toast.makeText(getActivity(), "Eanbleing dual network connectivity.",
				Toast.LENGTH_LONG).show();
		// get NetworkManager instance
		NetworkManager nm = NetworkManager.getInstance();
		// try to enable dual networking
		nm.enableDualNetworking();
		// only keep switch on if DN was really turned on
		//this.switchDualNetworking.setChecked(nm.isDualNetworkingEnabled());
	}

	public void stopDualNetworking()
	{
		Toast.makeText(getActivity(), "Disableing dual network connectivity.",
				Toast.LENGTH_LONG).show();
		// get NetworkManager instance
		NetworkManager nm = NetworkManager.getInstance();
		// try to disable dual networking
		nm.disableDualNetworking();
	}

	/**
	 * checks if root access is possible and tries to get root access for this
	 * app.
	 * 
	 * @return true/false
	 */
	public boolean checkRootAvailability()
	{
		if (RootTools.isAccessGiven())
		{
			Log.i(LTAG, "Root access granted");
			return true;
		}
		Toast.makeText(getActivity(),
				"ERROR: Root access not possible on device!", Toast.LENGTH_LONG)
				.show();
		Log.e(LTAG, "Root access not possible");
		return false;
	}

	/**
	 * checks for busybox (command line tool) availability
	 * 
	 * @return true/false
	 */
	public boolean checkBusyBoxAvailability()
	{
		if (RootTools.isBusyboxAvailable())
		{
			Log.i(LTAG, "Busybox is available.");
			return true;
		}

		Toast.makeText(getActivity(),
				"ERROR: Busybox is not installed on device!", Toast.LENGTH_LONG)
				.show();
		Log.e(LTAG, "Busybox is NOT available");
		return false;
	}

}
