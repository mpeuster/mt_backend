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

	private Handler monitoringHandler = new Handler();
	// TODO: move to an own class
	private Runnable monitoringTask = new Runnable()
	{
		public void run()
		{
			Log.v("PeriodicTimerService", "Awake with interval: "
					+ MONITORING_INTERVAL);
			monitoringHandler.postDelayed(monitoringTask, MONITORING_INTERVAL);
		}
	};

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
		monitoringHandler.removeCallbacks(monitoringTask);
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
					"pref_monitoring_intervall", "0"));
		} catch (Exception e)
		{
			Log.e(LTAG, "Error reading preferences. Using fallback.");
			Toast.makeText(getApplicationContext(),
					"Error reading preferences. Check your inputs.",
					Toast.LENGTH_LONG).show();
			MONITORING_INTERVAL = 1000;
		}

		// start monitoring task
		if (!monitoringHandler.hasMessages(0))
		{
			monitoringHandler.postDelayed(monitoringTask, MONITORING_INTERVAL);
			Log.d(LTAG, "Monitoring task started");
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
