package de.upb.upbmonitor;

import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;


public class MonitoringFragment extends Fragment {
    /**
     * Returns a new instance of this fragment for the given section
     * number.
     */
    public static MonitoringFragment newInstance() {
        MonitoringFragment fragment = new MonitoringFragment();
        return fragment;
    }

    public MonitoringFragment() {
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.fragment_monitoring, container, false);

        return rootView;
    }

}
