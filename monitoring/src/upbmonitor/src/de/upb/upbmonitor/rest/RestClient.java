package de.upb.upbmonitor.rest;

import android.util.Log;

public abstract class RestClient
{
	private static final String LTAG = "RestClient";
	
	private String mHost;
	private int mPort;
	
	public RestClient(String host, int port)
	{
		this.mHost = host;
		this.mPort = port;
	}
	
	private void send(String data)
	{
		
	}
	
	public void post(String data)
	{
		Log.w(LTAG, "HTTP post not implemented yet.");
	}
	
	public void put(String data)
	{
		Log.w(LTAG, "HTTP put not implemented yet.");
	}
	
	public void get(String data)
	{
		Log.w(LTAG, "HTTP get not implemented yet.");
	}
	
	public void delete(String data)
	{
		Log.w(LTAG, "HTTP delte not implemented yet.");
	}

}
