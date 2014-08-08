package de.upb.upbmonitor.monitoring.model;

public class UeContext
{
	/**
	 * Tread UE context as singelton class
	 */

	private static UeContext INSTANCE;
	private boolean CONTEXT_CHANGED;

	private int mUpdateCount;

	public synchronized int getUpdateCount()
	{
		return mUpdateCount;
	}

	public synchronized void incrementUpdateCount()
	{
		this.mUpdateCount++;
	}

	private boolean mDisplayState;

	public synchronized boolean isDisplayOn()
	{
		return mDisplayState;
	}

	public synchronized void setDisplayState(boolean mDisplayState)
	{
		if (mDisplayState != this.mDisplayState)
			this.setDataChangedFlag();
		this.mDisplayState = mDisplayState;
	}

	private String mActiveApplicationPackage;

	public synchronized String getActiveApplicationPackage()
	{
		return mActiveApplicationPackage;
	}

	public synchronized void setActiveApplicationPackage(
			String mActiveApplicationPackage)
	{
		if (!mActiveApplicationPackage.equals(this.mActiveApplicationPackage))
			this.setDataChangedFlag();
		this.mActiveApplicationPackage = mActiveApplicationPackage;
	}

	private String mActiveApplicationActivity;

	public synchronized String getActiveApplicationActivity()
	{
		return mActiveApplicationActivity;
	}

	public synchronized void setActiveApplicationActivity(
			String mActiveApplicationActivity)
	{
		if (!mActiveApplicationActivity.equals(this.mActiveApplicationActivity))
			this.setDataChangedFlag();
		this.mActiveApplicationActivity = mActiveApplicationActivity;
	}

	public synchronized long getTotalRxBytes()
	{
		NetworkTraffic nt = NetworkTraffic.getInstance();
		return nt.getTotalRxBytes();
	}

	public synchronized long getTotalTxBytes()
	{
		NetworkTraffic nt = NetworkTraffic.getInstance();
		return nt.getTotalTxBytes();
	}

	public synchronized long getMobileRxBytes()
	{
		NetworkTraffic nt = NetworkTraffic.getInstance();
		return nt.getMobileRxBytes();
	}

	public synchronized long getMobileTxBytes()
	{
		NetworkTraffic nt = NetworkTraffic.getInstance();
		return nt.getMobileTxBytes();
	}

	public synchronized long getWifiRxBytes()
	{
		NetworkTraffic nt = NetworkTraffic.getInstance();
		return nt.getWifiRxBytes();
	}

	public synchronized long getWifiTxBytes()
	{
		NetworkTraffic nt = NetworkTraffic.getInstance();
		return nt.getWifiTxBytes();
	}

	public synchronized static UeContext getInstance()
	{
		if (INSTANCE == null)
			INSTANCE = new UeContext();
		return INSTANCE;
	}

	public UeContext()
	{
		// value initialization
		this.CONTEXT_CHANGED = false;
		this.mUpdateCount = 0;
		this.mDisplayState = false;
		this.mActiveApplicationPackage = null;
		this.mActiveApplicationActivity = null;
	}

	public void resetDataChangedFlag()
	{
		NetworkTraffic nt = NetworkTraffic.getInstance();
		nt.resetDataChangedFlag();
		this.CONTEXT_CHANGED = false;
	}

	public void setDataChangedFlag()
	{
		this.CONTEXT_CHANGED = true;
	}

	public boolean hasChanged()
	{
		NetworkTraffic nt = NetworkTraffic.getInstance();
		return this.CONTEXT_CHANGED || nt.hasChanged();
	}
}
