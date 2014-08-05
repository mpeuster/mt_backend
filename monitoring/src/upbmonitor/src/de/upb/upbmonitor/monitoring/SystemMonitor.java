package de.upb.upbmonitor.monitoring;

import java.util.List;

import de.upb.upbmonitor.monitoring.model.UeContext;
import android.app.ActivityManager;
import android.app.ActivityManager.RunningTaskInfo;
import android.content.ComponentName;
import android.content.Context;
import android.os.PowerManager;
import android.util.Log;

public class SystemMonitor
{
	private static final String LTAG = "SystemMonitor";
	private Context myContext;

	public SystemMonitor(Context myContext)
	{
		this.myContext = myContext;
	}

	public void monitor()
	{
		this.monitorActiveApplication();
		this.monitorScreenState();
	}

	/**
	 * screen state monitoring
	 */
	public void monitorScreenState()
	{
		// get screen state from power model
		PowerManager pm = (PowerManager) this.myContext
				.getSystemService(Context.POWER_SERVICE);
		boolean screen_state = pm.isScreenOn();
		// write results to model
		UeContext c = UeContext.getInstance();
		c.setDisplayState(screen_state);
	}

	/**
	 * active application monitoring
	 */
	public void monitorActiveApplication()
	{
		// get activity manager and receive info
		ActivityManager am = (ActivityManager) this.myContext
				.getSystemService(Context.ACTIVITY_SERVICE);

		// get the info from the currently running task
		try
		{
			// receives task list with max_tasks = 1 and fetches the first
			// element of the list
			RunningTaskInfo taskInfo = am.getRunningTasks(1).get(0);

			// write results to model
			UeContext c = UeContext.getInstance();
			c.setActiveApplicationPackage(taskInfo.topActivity.getPackageName());
			c.setActiveApplicationActivity(taskInfo.topActivity.getClassName());
		} catch (Exception e)
		{
			Log.w(LTAG, "Not able to get running task info: " + e.getMessage());
		}
	}

}
