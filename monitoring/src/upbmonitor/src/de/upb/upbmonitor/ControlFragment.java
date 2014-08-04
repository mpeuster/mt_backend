package de.upb.upbmonitor;

import de.upb.upbmonitor.monitoring.MonitoringService;
import android.support.v4.app.Fragment;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CompoundButton;
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
						{
							Log.i(LTAG, "Dual networking turned on");
						} else
						{
							Log.i(LTAG, "Dual networking turned off");
						}
					}
				});

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

}
