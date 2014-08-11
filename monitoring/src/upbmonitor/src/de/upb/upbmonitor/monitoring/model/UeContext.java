package de.upb.upbmonitor.monitoring.model;

import org.json.JSONObject;

public class UeContext
{
	/**
	 * Tread UE context as singelton class
	 */

	private static UeContext INSTANCE;
	private boolean CONTEXT_CHANGED;

	private boolean mIsRegistered = false;
	
	
	public synchronized boolean isRegistered()
	{
		return mIsRegistered;
	}

	public synchronized void setRegistered(boolean mIsRegistered)
	{
		this.mIsRegistered = mIsRegistered;
	}

	private int mUpdateCount;

	public synchronized int getUpdateCount()
	{
		return mUpdateCount;
	}

	public synchronized void incrementUpdateCount()
	{
		this.mUpdateCount++;
	}
	
	private String mUuid;
	
	public synchronized String getUuid()
	{
		return mUuid;
	}

	public synchronized void setUuid(String mUuid)
	{
		// no change indicator here, since it is only set once
		// and the network controller knows this value
		this.mUuid = mUuid;
	}

	private String mDeviceID;
	
	public synchronized String getDeviceID()
	{
		return mDeviceID;
	}

	public synchronized void setDeviceID(String mDeviceID)
	{
		if (!mDeviceID.equals(this.mDeviceID))
			this.setDataChangedFlag();
		this.mDeviceID = mDeviceID;
	}
	
	private String mLocationServiceID;
	
	public synchronized String getLocationServiceID()
	{
		return mLocationServiceID;
	}

	public synchronized void setLocationServiceID(String mLocationServiceID)
	{
		if (!mLocationServiceID.equals(this.mLocationServiceID))
			this.setDataChangedFlag();
		this.mLocationServiceID = mLocationServiceID;
	}
	
	private String mWifiMac;
	
	public synchronized String getWifiMac()
	{
		return mWifiMac;
	}

	public synchronized void setWifiMac(String mWifiMac)
	{
		if (!mWifiMac.equals(this.mWifiMac))
			this.setDataChangedFlag();
		this.mWifiMac = mWifiMac;
	}
	
	private int mPositionX;

	public synchronized int getPositionX()
	{
		return mPositionX;
	}

	public synchronized void setPositionX(int mPositionX)
	{
		if (mPositionX != this.mPositionX)
			this.setDataChangedFlag();
		this.mPositionX = mPositionX;
	}
	
	private int mPositionY;

	public synchronized int getPositionY()
	{
		return mPositionY;
	}

	public synchronized void setPositionY(int mPositionY)
	{
		if (mPositionY != this.mPositionY)
			this.setDataChangedFlag();
		this.mPositionY = mPositionY;
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
	
	public synchronized float getTotalRxBytesPerSecond()
	{
		NetworkTraffic nt = NetworkTraffic.getInstance();
		return nt.getTotalRxBytesPerSecond();
	}

	public synchronized float getTotalTxBytesPerSecond()
	{
		NetworkTraffic nt = NetworkTraffic.getInstance();
		return nt.getTotalTxBytesPerSecond();
	}

	public synchronized float getMobileRxBytesPerSecond()
	{
		NetworkTraffic nt = NetworkTraffic.getInstance();
		return nt.getMobileRxBytesPerSecond();
	}

	public synchronized float getMobileTxBytesPerSecond()
	{
		NetworkTraffic nt = NetworkTraffic.getInstance();
		return nt.getMobileTxBytesPerSecond();
	}

	public synchronized float getWifiRxBytesPerSecond()
	{
		NetworkTraffic nt = NetworkTraffic.getInstance();
		return nt.getWifiRxBytesPerSecond();
	}

	public synchronized float getWifiTxBytesPerSecond()
	{
		NetworkTraffic nt = NetworkTraffic.getInstance();
		return nt.getWifiTxBytesPerSecond();
	}

	/**
	 * Use as singleton class.
	 * @return class instance
	 */
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
	
	/**
	 * JSON Tag names
	 */
	private static final String JSON_DEVICE_ID = "device_id";
	private static final String JSON_LOCATIONSERVICE_ID = "location_service_id";
	private static final String JSON_POSITION_X = "position_x";
	private static final String JSON_POSITION_Y = "position_y";
	private static final String JSON_DISPLAY_STATE = "display_state";
	private static final String JSON_ACTIVE_APPLICATION_PACKAGE = "active_application";
	private static final String JSON_ACTIVE_APPLICATION_ACTIVITY = "active_application_activity";
	private static final String JSON_WIFI_MAC = "wifi_mac";
	
	
	/**
	 * Generate JSON from context model object.
	 * @return JSONObject
	 */
	public JSONObject toJson()
	{
		//TODO create JSON object
		
		return null;
		
	}
}
