package de.upb.upbmonitor.monitoring;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.util.Log;

public class MonitoringService extends Service
{
	private static final String LTAG = "MonitoringService";
	
	@Override
	public void onCreate()
	{
		super.onCreate();
		Log.d(LTAG, "onCreate()");
	}

	@Override
	public void onDestroy()
	{
		super.onDestroy();
		Log.d(LTAG, "onDestroy()");
	}

	@Override
	public int onStartCommand(Intent intent, int flags, int startId)
	{
		Log.d(LTAG, "onStartCommand()");
		// TODO do something useful
		return Service.START_STICKY;
	}

	@Override
	public IBinder onBind(Intent intent)
	{
		// TODO for communication return IBinder implementation
		return null;
	}
}