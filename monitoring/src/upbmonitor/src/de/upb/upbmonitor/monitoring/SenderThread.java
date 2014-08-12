package de.upb.upbmonitor.monitoring;

import android.content.Context;
import android.os.Handler;
import android.os.PowerManager;
import android.util.Log;
import android.widget.Toast;
import de.upb.upbmonitor.monitoring.model.UeContext;
import de.upb.upbmonitor.rest.UeEndpoint;

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
	private UeEndpoint restUeEndpoint = null;

	public SenderThread(Context myContext, Handler myHandler,
			int monitoringInterval, String backendHost, int backendPort)
	{ 
		// arguments
		this.myContext = myContext;
		this.myHandler = myHandler;
		this.mSenderInterval = monitoringInterval;
		
		// initializations
		// API end point
		this.restUeEndpoint = new UeEndpoint(backendHost, backendPort);
	}

	public void run()
	{
		Log.v(LTAG, "Awake with interval: " + this.mSenderInterval);
		// access model
		UeContext c = UeContext.getInstance();
		
		if(!c.isRegistered())
		{
			// register UE in backend
			this.restUeEndpoint.register();
			c.setRegistered(true);
		}
		else if (c.getURI() != null)
		{
			// periodically send update if UE is registered		
			this.sendUpdate();
		}
		else
		{
			// something went wrong with the register operation
			Toast.makeText(myContext,
					"Backend connection error.",
					Toast.LENGTH_SHORT).show();
			// trigger re-register
			c.setRegistered(false);
		}
		myHandler.postDelayed(this, this.mSenderInterval);
	}

	private void sendUpdate()
	{
		// access model
		UeContext c = UeContext.getInstance();

		// send context update if new data is available (context has changed)
		if (c.hasChanged())
		{
			// detailed log output:
			Log.v(LTAG, c.toString());
			
			// send to backend
			this.restUeEndpoint.update();

			// reset changed flag in all models
			c.resetDataChangedFlag();
		}
	}
	
	public void removeUe()
	{
		// access model
		UeContext c = UeContext.getInstance();
		// remove UE from backend
		this.restUeEndpoint.remove();
		c.setRegistered(false);
	}
}
