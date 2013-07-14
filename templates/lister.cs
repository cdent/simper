<ul class="page_list">
    <?cs each:page = listables ?>
    <li>
        <a href="/content/name/<?cs var:page.name ?>">
            <?cs var:page.name ?>
        </a>
    | <?cs var:page.mod_time ?>
    <?cs if:page.count ?> | <?cs var:page.count ?><?cs /if ?>
        <?cs each:associate = page.associates ?>
            - <a href="/content/name/<?cs var:associate.name ?>">
                <?cs var:associate.name ?></a>
        <?cs /each ?>
    </li>
    <?cs /each ?>
</ul>
