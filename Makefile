build: node_modules lint
	node build

serve: node_modules
	node build serve

deploy: node_modules lint
	node build publish

node_modules: package.json
	npm install

lint:
	npm run lint

clean:
	rm -rf node_modules build

.PHONY: build
