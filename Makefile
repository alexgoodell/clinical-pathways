MSG=auto_backup

backup:
	( \
		source ~/.virtualenvs/pathways/bin/activate; \
		poetry check; \
    )
	git add .
	git commit -m "$(MSG)"
	git push origin main

remote up:
	git pull
	docker compose up -d

remote down:
	git pull
	docker compose down -d

serve:
	python app/__init__.py

destroy:


.PHONY: backup remote