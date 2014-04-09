#! /usr/bin/env python

import api
import logging
import py_meter_ingest_email

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('py_meter_ingest.log')
fh.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


if __name__ == '__main__':

    # Create instance of Rhyno to use for ingesting/publishing, point it to production host.
    r = api.Rhyno(host='http://api.plosjournals.org/v1/')

    ingested=[]
    failed_ingest={}
    #Ingest article zips on Production. If succeed, write to new list of ingested articles.
    for article in r.ingestibles():
        if article[-4:] == '.zip':
            try:
                r.ingest(article, force_reingest=True)
                ingested.append(str(article))
                logger.info('Ingested ' + str(article) + ' on production server')
            except Exception, e:
                #If fails, write to list of error articles with exception, and send that list as email to webprod.
                failed_ingest[str(article)] = str(e)
                logger.error('Issue ingesting ' + str(article) + ' on production, '+str(e))

    # Send emails of ingestion results.
    # First create message body from dict that email will accept.
    try:
        message = 'Ingested:\n\n'
        for doi in ingested:
            message += doi + '\n'
        message += '\nIngest Errors:\n'
        for key in failed_ingest.keys():
            message += key + ': ' + failed_ingest[key] + '\n'
        py_meter_ingest_email.send_mail(message, 'Ingest Results')
    except Exception, e:
        logger.error("Error sending Ingest Results email, "+str(e))


    failed_publish = {}
    #Publish and syndicate articles in ingested list
    for article in ingested:
        doi = '10.1371/journal.'+article[:-4]
        try:
            r.production_publish(doi)
        except Exception, e:
            failed_publish[doi] = str(e)
    try:
        # Send email of failed-to-publish articles if any exist.
        if len(failed_publish) > 1:
            pub_message_errors = 'Publish Errors:\n\n'
            for key in failed_publish.keys():
                pub_message_errors += key + ': ' + failed_publish[key] + '\n'
            py_meter_ingest_email.send_mail(message, 'Publish Errors')
    except Exception, e:
        logger.error("Error sending Publish Errors email, "+str(e))

