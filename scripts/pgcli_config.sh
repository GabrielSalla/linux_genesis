sed -i '/^pager = /c\pager = pspg -ibc0FX --line-numbers' ~/.config/pgcli/config
sed -i '/\[named queries\]/r ./templates/pgcli_named_queries' ~/.config/pgcli/config
