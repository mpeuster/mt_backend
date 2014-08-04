package de.upb.upbmonitor.monitoring;

import android.content.Context;
import android.os.Handler;
import android.os.PowerManager;
import android.util.Log;
import de.upb.upbmonitor.monitoring.model.UeContext;

public class MonitoringThread implements Runnable
{
	private static final String LTAG = "MonitoringThread";
	private Context myContext;
	private Handler myHandler;
	private int mMonitoringInterval;

	public MonitoringThread(Context myContext, Handler myHandler,
			int monitoringInterval)
	{
		this.myContext = myContext;
		this.myHandler = myHandler;
		Log.d(LTAG, "MMM:" + monitoringInterval);
		this.mMonitoringInterval = monitoringInterval;
	}

	public void run()
	{
		Log.v("PeriodicTimerService", "Awake with interval: "
				+ this.mMonitoringInterval);
		this.monitor();
		myHandler.postDelayed(this, this.mMonitoringInterval);
	}

	private void monitor()
	{
		// get screen state
		PowerManager pm = (PowerManager) this.myContext
				.getSystemService(Context.POWER_SERVICE);
		boolean screen_state = pm.isScreenOn();
		// update model
		UeContext c = UeContext.getInstance();
		c.setDisplayState(screen_state);
		c.incrementUpdateCount();

		// print out if new data is available (context has changed)
		if (c.hasChanged())
		{
			Log.i(LTAG, "UpdateCount: " + c.getUpdateCount());
			Log.i(LTAG, "Display state: " + c.isDisplayOn());
			c.resetDataChangedFlag();
		}
	}
}
