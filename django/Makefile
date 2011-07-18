vm:
	@vagrant destroy && vagrant up

provision:
	@provy -s local.web -p vagrant mysql_password=pass

provision-prod:
	@provy -s prod.web -p vagrant mysql_password=pass
