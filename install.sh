zip -r fah-plasmoid.zip applet/*
zip -r fah-plasmoid-data-engine.zip data-engine/*
plasmapkg -t dataengine -i fah-plasmoid-data-engine.zip
plasmapkg -i fah-plasmoid.zip
rm fah-plasmoid.zip
rm fah-plasmoid-data-engine.zip
plasma-windowed fah-plasmoid
