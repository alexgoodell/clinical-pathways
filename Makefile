MSG=auto_backup

backup:
	( \
		source ~/.virtualenvs/pathways/bin/activate; \
		pip install --upgrade pip; \
		pip freeze > requirements.txt; \
    )
	git add .
	git commit -m "$(MSG)"
	git push origin main


.PHONY: backup