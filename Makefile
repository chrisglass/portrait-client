ACCOUNT="devel"

check:
	@nosetests3 portrait

clean:
	@find -name "*.pyc" -delete
	@rm -rf _trial_temp

run:
	@echo Registering against account $(ACCOUNT)
	@python3 -m portrait $(ACCOUNT) example_config.conf
