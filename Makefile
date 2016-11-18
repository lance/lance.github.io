build: node_modules lint
	node build

serve: node_modules
	node build serve 2>&1 | tee server.log &
	sleep 3
	open http://localhost:8080

deploy: node_modules lint
	node build publish

node_modules: package.json
	npm install

lint:
	npm run lint

clean:
	rm -rf node_modules build

.PHONY: build
