package de.upb.upbmonitor.monitoring;

import de.upb.upbmonitor.monitoring.model.UeContext;
import android.content.Context;
import android.os.PowerManager;

public class SystemMonitor
{
	private Context myContext;
	
	public SystemMonitor(Context myContext)
	{
		this.myContext = myContext;
	}
	
	
	public void monitor()
	{
		// get screen state
		PowerManager pm = (PowerManager) this.myContext
				.getSystemService(Context.POWER_SERVICE);
		boolean screen_state = pm.isScreenOn();
		// update model
		UeContext c = UeContext.getInstance();
		c.setDisplayState(screen_state);
		
		// TODO add monitoring of active application
	}
}
