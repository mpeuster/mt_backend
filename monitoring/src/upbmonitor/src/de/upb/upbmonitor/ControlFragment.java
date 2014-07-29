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

	private View rootView;
	private Switch switchMonitoringService;
	private Switch switchDualNetworking;

	/**
	 * Returns a new instance of this fragment for the given section number.
	 */
	public static ControlFragment newInstance()
	{
		ControlFragment fragment = new ControlFragment();
		return fragment;
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

		// TODO set switch states based on system state

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

	private void startMonitoringService()
	{
		Intent i = new Intent(this.getActivity(), MonitoringService.class);
		//i.putExtra("name", "SurvivingwithAndroid");
		this.getActivity().startService(i);
		Log.i(LTAG, "Monitoring switch turned on");
	}

	private void stopMonitoringService()
	{
		Intent i = new Intent(this.getActivity(), MonitoringService.class);
		this.getActivity().stopService(i);
		Log.i(LTAG, "Monitoring switch turned off");
	}

}
