ACCOUNT="devel"

check:
	@nosetests3 landscape

clean:
	@find -name "*.pyc" -delete
	@rm -rf _trial_temp

run:
	@echo Registering against account $(ACCOUNT)
	@python3 -m landscape $(ACCOUNT) example_config.conf
