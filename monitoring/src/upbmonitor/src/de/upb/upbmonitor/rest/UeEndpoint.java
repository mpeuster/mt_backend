package de.upb.upbmonitor.rest;

import de.upb.upbmonitor.monitoring.model.UeContext;

public class UeEndpoint extends RestClient
{
	private static final String LTAG = "UeEndpoint";

	public UeEndpoint(String host, int port)
	{
		super(host, port);
	}

	public void registerUe()
	{
		// access model
		UeContext c = UeContext.getInstance();

		c.setRegistered(true);

		this.post("bla");
	}

	public void removeUe()
	{
		// access model
		UeContext c = UeContext.getInstance();

		this.delete("bla");
		
		c.setRegistered(false);

	}

}
