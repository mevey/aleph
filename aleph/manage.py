# coding: utf-8
import os
import logging

from flask.ext.script import Manager
from flask.ext.assets import ManageAssets
from flask.ext.migrate import MigrateCommand

from aleph.core import create_app
from aleph.model import db, upgrade_db, Source, Document
from aleph.views import mount_app_blueprints, assets
from aleph.analyze import analyze_source
from aleph.alerts import check_alerts
from aleph.index import init_search, delete_index, upgrade_search
from aleph.index import index_document
from aleph.ext import get_crawlers
from aleph.crawlers.directory import DirectoryCrawler
from aleph.crawlers.sql import SQLCrawler
from aleph.crawlers.mf import MetaFolderCrawler


log = logging.getLogger('aleph')

app = create_app()
mount_app_blueprints(app)
manager = Manager(app)
manager.add_command('assets', ManageAssets(assets))
manager.add_command('db', MigrateCommand)


@manager.command
def sources():
    """List all sources."""
    for source in Source.all():
        print source.id, source.foreign_id, source.label


@manager.command
def alerts():
    """Generate alert notifications."""
    check_alerts.delay()


@manager.command
def crawl(name):
    """Execute the given crawler."""
    log.info('Crawling %r...', name)
    crawlers = get_crawlers()
    if name not in crawlers:
        log.info('No such crawler: %r', name)
    else:
        crawler = crawlers.get(name)()
        crawler.execute()
    db.session.commit()


@manager.command
@manager.option('-s', '--source', dest='source')
@manager.option('-l', '--language', dest='language', nargs='*')
@manager.option('-c', '--country', dest='country', nargs='*')
def crawldir(directory, source=None, language=None, country=None):
    """Crawl the given directory."""
    directory = os.path.abspath(directory)
    directory = os.path.normpath(directory)
    log.info('Crawling %r...', directory)
    meta = {}
    if language is not None:
        meta['languages'] = [language]
    if country is not None:
        meta['countries'] = [country]
    crawler = DirectoryCrawler(base_meta=meta)
    crawler.execute(directory=directory, source=source)


@manager.command
@manager.option('-s', '--source', dest='source')
def crawlsql(yaml_config, source=None):
    """Crawl the given database query file."""
    yaml_config = os.path.abspath(yaml_config)
    yaml_config = os.path.normpath(yaml_config)
    log.info('Crawling %r...', yaml_config)
    SQLCrawler().execute(config=yaml_config, source=source)
    db.session.commit()


@manager.command
@manager.option('-s', '--source', dest='source')
def metafolder(folder, source=None):
    """Crawl the given metafolder path."""
    log.info('Importing %r...', folder)
    MetaFolderCrawler().execute(folder=folder, source=source)
    db.session.commit()


@manager.command
def flush(foreign_id):
    """Reset the crawler state for a given source specification."""
    from aleph.index import delete_source
    source = Source.by_foreign_id(foreign_id)
    if source is None:
        raise ValueError("No such source: %r" % foreign_id)
    delete_source(source.id)
    source.delete()
    db.session.commit()


@manager.command
def analyze(foreign_id=None):
    """Re-analyze documents in the given source (or throughout)."""
    if foreign_id:
        source = Source.by_foreign_id(foreign_id)
        if source is None:
            raise ValueError("No such source: %r" % foreign_id)
        analyze_source.delay(source.id)
    else:
        for source in Source.all():
            analyze_source.delay(source.id)


@manager.command
def index(foreign_id=None):
    """Index documents in the given source (or throughout)."""
    q = Document.all_ids()
    if foreign_id:
        source = Source.by_foreign_id(foreign_id)
        if source is None:
            raise ValueError("No such source: %r" % foreign_id)
        q = q.filter(Document.source_id == source.id)
    else:
        delete_index()
        init_search()
    for doc_id, in q:
        index_document.delay(doc_id)


@manager.command
def upgrade():
    """Create or upgrade the search index and database."""
    upgrade_db()
    upgrade_search()


@manager.command
def evilshit():
    """Delete all data and recreate the database."""
    db.drop_all()
    upgrade_db()
    delete_index()
    init_search()


def main():
    manager.run()


if __name__ == "__main__":
    main()
