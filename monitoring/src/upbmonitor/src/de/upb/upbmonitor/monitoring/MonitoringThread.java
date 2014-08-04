package de.upb.upbmonitor.monitoring;

import android.content.Context;
import android.os.Handler;
import android.os.PowerManager;
import android.util.Log;
import de.upb.upbmonitor.monitoring.model.UeContext;

/**
 * Represents the monitoring thread of the service.
 * 
 * Attention: This Runnable/Handler implementation is the way to do periodic
 * tasks in Android. Do not use Java timers. However its a bit ugly.
 * 
 * @author manuel
 * 
 */
public class MonitoringThread implements Runnable
{
	private static final String LTAG = "MonitoringThread";
	private Context myContext;
	private Handler myHandler;
	private int mMonitoringInterval;
	
	private SystemMonitor mSystemMonitor;

	public MonitoringThread(Context myContext, Handler myHandler,
			int monitoringInterval)
	{	// arguments
		this.myContext = myContext;
		this.myHandler = myHandler;
		this.mMonitoringInterval = monitoringInterval;
		
		// initializations
		this.mSystemMonitor = new SystemMonitor(this.myContext);		
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
		this.mSystemMonitor.monitor();

		// update model
		UeContext c = UeContext.getInstance();
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
