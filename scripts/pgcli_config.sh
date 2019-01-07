sed -i '/^pager = /c\pager = pspg -ibc0FX --line-numbers --no-commandbar --no-mouse' ~/.config/pgcli/config
sed -i '/\[named queries\]/r ./templates/pgcli_named_queries' ~/.config/pgcli/config
