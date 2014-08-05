package de.upb.upbmonitor.monitoring;

import android.app.Service;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Handler;
import android.os.IBinder;
import android.preference.PreferenceManager;
import android.util.Log;
import android.widget.Toast;

public class MonitoringService extends Service
{
	private static final String LTAG = "MonitoringService";
	public static boolean SERVICE_EXISTS = false;
	private static int MONITORING_INTERVAL = Integer.MAX_VALUE;
	private static int SENDING_INTERVAL = Integer.MAX_VALUE;

	private Handler threadHandler = new Handler();
	private Runnable monitoringTask = null;
	private Runnable sendingTask = null;

	@Override
	public void onCreate()
	{
		super.onCreate();
		SERVICE_EXISTS = true;
		Log.d(LTAG, "onCreate()");
	}

	@Override
	public void onDestroy()
	{
		super.onDestroy();
		Log.d(LTAG, "onDestroy()");
		threadHandler.removeCallbacks(monitoringTask);
		threadHandler.removeCallbacks(sendingTask);
		SERVICE_EXISTS = false;
	}

	@Override
	public int onStartCommand(Intent intent, int flags, int startId)
	{
		Log.d(LTAG, "onStartCommand()");
		// load preferences
		try
		{
			SharedPreferences preferences = PreferenceManager
					.getDefaultSharedPreferences(this);
			MONITORING_INTERVAL = Integer.valueOf(preferences.getString(
					"pref_monitoring_interval", "0"));
			SENDING_INTERVAL = Integer.valueOf(preferences.getString(
					"pref_sending_interval", "0"));
		} catch (Exception e)
		{
			// if preferences could not be read, use a fixed interval
			Log.e(LTAG, "Error reading preferences. Using fallback.");
			Toast.makeText(getApplicationContext(),
					"Error reading preferences. Check your inputs.",
					Toast.LENGTH_LONG).show();
			MONITORING_INTERVAL = 1000;
			SENDING_INTERVAL = 5000;
		}

		// run service's tasks
		if (!threadHandler.hasMessages(0))
		{
			// start monitoring task
			this.monitoringTask = new MonitoringThread(this,
					this.threadHandler, MONITORING_INTERVAL);
			threadHandler.postDelayed(monitoringTask, 0);
			Log.d(LTAG, "Monitoring task started");
			
			// start monitoring task
			this.sendingTask = new SenderThread(this,
					this.threadHandler, SENDING_INTERVAL);
			threadHandler.postDelayed(sendingTask, 0);
			Log.d(LTAG, "Sender task started");
		}
		// start sticky, so service will be restarted if it is killed
		return Service.START_STICKY;
	}

	@Override
	public IBinder onBind(Intent intent)
	{
		// TODO for communication return IBinder implementation
		return null;
	}
}
