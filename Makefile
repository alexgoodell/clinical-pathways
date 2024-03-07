MSG=auto_backup

backup:
	( \
		source ~/.virtualenvs/pathways/bin/activate; \
		poetry check; \
    )
	git add .
	git commit -m "$(MSG)"
	git push origin main


.PHONY: backup