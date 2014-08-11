package de.upb.upbmonitor.monitoring;

import android.content.Context;
import android.os.Handler;
import android.os.PowerManager;
import android.util.Log;
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
			this.restUeEndpoint.registerUe();
		}
		else
		{
			// periodically send update if UE is registered		
			this.sendUpdate();
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
			// TODO implement json client to update contexts
			// system values
			Log.i(LTAG, "UpdateCount: " + c.getUpdateCount());
			Log.i(LTAG, "Display state: " + c.isDisplayOn());
			Log.i(LTAG, "Active package: " + c.getActiveApplicationPackage());
			Log.i(LTAG, "Active activity: " + c.getActiveApplicationActivity());
			// network values
			Log.i(LTAG,
					"Mobile Traffic:\tRx:" + c.getMobileRxBytes() + "\tTx:"
							+ c.getMobileTxBytes() + "\tRx/s:"
							+ c.getMobileRxBytesPerSecond() + " \tTx/s:"
							+ c.getMobileTxBytesPerSecond());
			Log.i(LTAG,
					"Wifi   Traffic:\tRx:" + c.getWifiRxBytes() + "\tTx:"
							+ c.getWifiTxBytes() + "\tRx/s:"
							+ c.getWifiRxBytesPerSecond() + " \tTx/s:"
							+ c.getWifiTxBytesPerSecond());
			Log.i(LTAG,
					"Total  Traffic:\tRx:" + c.getTotalRxBytes() + "\tTx:"
							+ c.getTotalTxBytes() + "\tRx/s:"
							+ c.getTotalRxBytesPerSecond() + " \tTx/s:"
							+ c.getTotalTxBytesPerSecond());

			// reset changed flag in all models
			c.resetDataChangedFlag();
		}
	}
	
	public void removeUe()
	{
		// register UE in backend
		this.restUeEndpoint.removeUe();
	}
}
