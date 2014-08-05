package de.upb.upbmonitor.monitoring;

import android.content.Context;
import android.os.Handler;
import android.os.PowerManager;
import android.util.Log;
import de.upb.upbmonitor.monitoring.model.UeContext;

/**
 * Represents the sender thread of the service.
 * 
 * Attention: This Runnable/Handler implementation is the way to do periodic
 * tasks in Android. Do not use Java timers. However its a bit ugly.
 * 
 * @author manuel
 * 
 */
public class SenderThread implements Runnable
{
	private static final String LTAG = "SenderThread";
	private Context myContext;
	private Handler myHandler;
	private int mSenderInterval;
	


	public SenderThread(Context myContext, Handler myHandler,
			int monitoringInterval)
	{	// arguments
		this.myContext = myContext;
		this.myHandler = myHandler;
		this.mSenderInterval = monitoringInterval;
		
		// initializations
	
	}

	public void run()
	{
		Log.v(LTAG, "Awake with interval: "
				+ this.mSenderInterval);
		// periodically send
		this.send();
		myHandler.postDelayed(this, this.mSenderInterval);
	}

	private void send()
	{
		// access model
		UeContext c = UeContext.getInstance();
	
		// send context update if new data is available (context has changed)
		if (c.hasChanged())
		{
			// TODO implement json client to update contexts
			Log.i(LTAG, "UpdateCount: " + c.getUpdateCount());
			Log.i(LTAG, "Display state: " + c.isDisplayOn());
			Log.i(LTAG, "Active package: " + c.getActiveApplicationPackage());
			Log.i(LTAG, "Active activity: " + c.getActiveApplicationActivity());
			c.resetDataChangedFlag();
		}
	}
}
