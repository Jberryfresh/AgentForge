AGENTS_FILE := AGENTS_persist.md

.PHONY: note persist-init

persist-init:
	@# Initialize the persistence file if missing
	@[ -f $(AGENTS_FILE) ] || echo "#+ Project Session Memory (Local)" > $(AGENTS_FILE)

note: persist-init
	@# Append a timestamped note. Usage: make note MSG="Short message"
	@if [ -z "$(MSG)" ]; then echo "Error: provide MSG=\"your note\""; exit 1; fi
	@{
	  printf "## %s — Note\n" "$(shell date -u +'%Y-%m-%d %H:%M UTC')";
	  printf "User intent: %s\n" "$(MSG)";
	  printf "Actions: -\n";
	  printf "Decisions/assumptions: -\n";
	  printf "Open items / next step: -\n\n";
	} >> $(AGENTS_FILE)

