all:

install:
	install -m 755 -o root -g root -d $(DESTDIR)/bitbot
	install -m 755 -o root -g root bitbot.py $(DESTDIR)/bitbot/bitbot.py
	install -m 755 -o root -g root rpcgw.py $(DESTDIR)/bitbot/rpcgw.py
