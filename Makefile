check:
	nosetests3 landscape

clean:
	@find -name "*.pyc" -delete
	@rm -rf _trial_temp

run:
	@python3 -m landscape chrisglass example_config.conf
