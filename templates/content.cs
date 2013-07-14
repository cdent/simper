<div class="content">
    <?cs var:text ?>
    <div class="mod_time">
        <?cs var:page.mod_time ?>
    </div>
    <div class="tags">
        <?cs each:tag = tags ?>
            <a href="/content/name/<?cs var:tag.name ?>">
                <?cs var:tag.name ?></a>
        <?cs /each ?>
    </div>
    <?cs if:text && page.mod_time ?>
        <?cs include:"templates/tagadd.cs" ?>
    <?cs /if ?>
    <div class="revisions">
        <?cs with:listables = pages ?>
            <?cs include:"templates/lister.cs" ?>
        <?cs /with ?>
    </div>
    <?cs if:len(comments) ?>
    <div class="comments">
        <h2>Comments</h2>
        <?cs include:"templates/comments.cs" ?>
    </div>
    <?cs /if ?>
    <?cs if:text && page.mod_time ?>
        <?cs include:"templates/commentadd.cs" ?>
    <?cs /if ?>
    <?cs if:len(associates) ?>
    <div class="associates">
        <h2>Back Associates</h2>
        <?cs with:listables = associates ?>
            <?cs include:"templates/lister.cs" ?>
        <?cs /with ?>
    </div>
    <?cs /if ?>
</div>
