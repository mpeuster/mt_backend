package de.upb.upbmonitor.monitoring.model;

import java.util.HashMap;
import java.util.Map;
import android.util.Log;

public class NetworkTraffic
{
	private static final String LTAG = "NetworkTrafficModel";

	public enum TType
	{
		TotalRx, TotalRxBackup, TotalTx, TotalTxBackup, MobileRx, MobileRxBackup, MobileTx, MobileTxBackup, WifiRx, WifiTx
	}

	private static NetworkTraffic INSTANCE;

	private Map<TType, Long> mBytes;
	private Map<TType, Long> mTimestamp;

	private synchronized void setBytes(TType t, long b)
	{
		// gather data
		TType tb = null; // backup type
		switch (t)
		{
		case TotalRx:
			tb = TType.TotalRxBackup;
			break;
		case TotalTx:
			tb = TType.TotalTxBackup;
			break;
		case MobileRx:
			tb = TType.MobileRxBackup;
			break;
		case MobileTx:
			tb = TType.MobileTxBackup;
			break;
		default:
			Log.e(LTAG, "Bad TType.");
			break;
		}

		if (tb != null)
		{
			// add data to model
			this.mBytes.put(tb, this.mBytes.get(t));
			this.mTimestamp.put(tb, this.mTimestamp.get(t));
			this.mBytes.put(t, b);
			this.mTimestamp.put(t, System.currentTimeMillis());
		}
	}

	public synchronized void setTotalRxBytes(long b)
	{
		this.setBytes(TType.TotalRx, b);
	}

	public synchronized void setTotalTxBytes(long b)
	{
		this.setBytes(TType.TotalTx, b);
	}

	public synchronized void setMobileRxBytes(long b)
	{
		this.setBytes(TType.MobileRx, b);
	}

	public synchronized void setMobileTxBytes(long b)
	{
		this.setBytes(TType.MobileTx, b);
	}

	private synchronized long getBytes(TType t)
	{
		// special case Wifi:
		// calculate values, since they are not available in the API
		// wifi = (total - mobile)
		if (t == TType.WifiRx)
			return this.mBytes.get(TType.TotalRx)
					- this.mBytes.get(TType.MobileRx);
		if (t == TType.WifiTx)
			return this.mBytes.get(TType.TotalTx)
					- this.mBytes.get(TType.MobileTx);
		return this.mBytes.get(t);
	}

	public synchronized long getTotalRxBytes()
	{
		return this.getBytes(TType.TotalRx);
	}

	public synchronized long getTotalTxBytes()
	{
		return this.getBytes(TType.TotalTx);
	}

	public synchronized long getMobileRxBytes()
	{
		return this.getBytes(TType.MobileRx);
	}

	public synchronized long getMobileTxBytes()
	{
		return this.getBytes(TType.MobileTx);
	}

	public synchronized long getWifiRxBytes()
	{
		return this.getBytes(TType.WifiRx);
	}

	public synchronized long getWifiTxBytes()
	{
		return this.getBytes(TType.WifiTx);
	}

	public synchronized static NetworkTraffic getInstance()
	{
		if (INSTANCE == null)
			INSTANCE = new NetworkTraffic();
		return INSTANCE;
	}

	public NetworkTraffic()
	{
		// initializations
		this.mBytes = new HashMap<TType, Long>();
		this.mBytes.put(TType.TotalRx, 0L);
		this.mBytes.put(TType.TotalTx, 0L);
		this.mBytes.put(TType.MobileRx, 0L);
		this.mBytes.put(TType.MobileTx, 0L);

		this.mTimestamp = new HashMap<TType, Long>();
		this.mBytes.put(TType.TotalRx, System.currentTimeMillis());
		this.mBytes.put(TType.TotalTx, System.currentTimeMillis());
		this.mBytes.put(TType.MobileRx, System.currentTimeMillis());
		this.mBytes.put(TType.MobileTx, System.currentTimeMillis());
	}
	
	public synchronized boolean hasChanged()
	{
		return true;
	}
	
	public void  resetDataChangedFlag()
	{
		//TODO implement threshold based change flag for network model
	}
	

}
