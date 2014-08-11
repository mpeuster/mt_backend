package de.upb.upbmonitor.rest;

import android.util.Log;
import de.upb.upbmonitor.monitoring.model.UeContext;

public class UeEndpoint extends RestClient
{
	private static final String LTAG = "UeEndpoint";

	public UeEndpoint(String host, int port)
	{
		super(host, port);
	}

	public void registerUe(UeContext c)
	{		
		Log.v(LTAG, c.toJson().toString());
		this.post("bla");
	}
	
	public void updateUe(UeContext c)
	{
		
	}

	public void removeUe(UeContext c)
	{
		this.delete("bla");
	}

}
