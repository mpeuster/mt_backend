package de.upb.upbmonitor;

import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;


public class ControlFragment extends Fragment {
    /**
     * Returns a new instance of this fragment for the given section
     * number.
     */
    public static ControlFragment newInstance() {
        ControlFragment fragment = new ControlFragment();
        return fragment;
    }

    public ControlFragment() {
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.fragment_control, container, false);

        return rootView;
    }

}
