package de.upb.upbmonitor;

import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CompoundButton;
import android.widget.LinearLayout;
import android.widget.NumberPicker;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.CompoundButton.OnCheckedChangeListener;

public class LocationFragment extends Fragment
{
	private static final String LTAG = "LocationFragment";

	private Switch switchManualLocation;
	private NumberPicker npPositionX, npPositionY;
	private TextView tvPH, tvPX, tvPY;

	/**
	 * Returns a new instance of this fragment for the given section number.
	 */
	public static LocationFragment newInstance()
	{
		LocationFragment fragment = new LocationFragment();
		return fragment;
	}

	public LocationFragment()
	{
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState)
	{
		View rootView = inflater.inflate(R.layout.fragment_location, container,
				false);

		// get pointers to control elements
		this.switchManualLocation = (Switch) rootView
				.findViewById(R.id.switchManualLocation);
		this.npPositionX = (NumberPicker) rootView
				.findViewById(R.id.npPositionX);
		this.npPositionY = (NumberPicker) rootView
				.findViewById(R.id.npPositionY);

		this.tvPH = (TextView) rootView.findViewById(R.id.textViewPHeadline);
		this.tvPX = (TextView) rootView.findViewById(R.id.textViewPX);
		this.tvPY = (TextView) rootView.findViewById(R.id.textViewPY);

		// TODO depended on property value
		this.setEnableToPositionControls(false);

		// fill number picker controls
		this.fillNumberPicker(this.npPositionX, 0, 2000, 100);
		this.fillNumberPicker(this.npPositionY, 0, 2000, 100);

		// manual location switch listener
		this.switchManualLocation
				.setOnCheckedChangeListener(new OnCheckedChangeListener()
				{

					@Override
					public void onCheckedChanged(CompoundButton buttonView,
							boolean isChecked)
					{
						if (isChecked)
						{
							setEnableToPositionControls(true);
							Log.i(LTAG, "Manual location enabled");
						} else
						{
							setEnableToPositionControls(false);
							Log.i(LTAG, "Manual location disabled");
						}
					}
				});

		return rootView;
	}

	private void setEnableToPositionControls(boolean b)
	{
		this.tvPH.setEnabled(b);
		this.tvPX.setEnabled(b);
		this.tvPY.setEnabled(b);
		this.npPositionX.setEnabled(b);
		this.npPositionY.setEnabled(b);
	}

	private void fillNumberPicker(NumberPicker np, int min, int max, int step)
	{
		int items = (max - min) / step + 1;
		String[] nums = new String[items];
		for (int i = 0; i < items; i++)
			nums[i] = Integer.toString(i * step);

		np.setDisplayedValues(nums);
		np.setMinValue(min);
		np.setMaxValue(items - 1);
		np.setValue(min);
	}

}
