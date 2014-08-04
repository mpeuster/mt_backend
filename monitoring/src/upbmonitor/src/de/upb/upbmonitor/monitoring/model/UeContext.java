package de.upb.upbmonitor.monitoring.model;

public class UeContext
{
	/**
	 * Tread UE context as singelton class
	 */

	private static UeContext INSTANCE;
	private boolean CONTEXT_CHANGED;

	private String mActiveApplication;

	public synchronized String getActiveApplication()
	{
		return mActiveApplication;
	}

	public synchronized void setActiveApplication(String mActiveApplication)
	{
		this.mActiveApplication = mActiveApplication;
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
		this.mActiveApplication = null;
		this.mUpdateCount = 0;
		this.mDisplayState = false;

	}

	public void resetDataChangedFlag()
	{
		this.CONTEXT_CHANGED = false;
	}

	public void setDataChangedFlag()
	{
		this.CONTEXT_CHANGED = true;
	}

	public boolean hasChanged()
	{
		return this.CONTEXT_CHANGED;
	}
}
