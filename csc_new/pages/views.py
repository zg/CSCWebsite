from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader

from pages.models import RenderableEvents, ExamReview
from github3 import GitHub
from github3.orgs import Organization

# Create your views here.

def generic(request):
	template = loader.get_template("pages%s.html" % request.path)
	context = RequestContext(request, {
		#Nothing really should go here
	})
	return HttpResponse(template.render(context))

def index(request):
	re = RenderableEvents()
	re.getEvents()
	template = loader.get_template("pages/index.html")
	context = RequestContext(request, {
		'events' : re.events,
	})
	return HttpResponse(template.render(context))
	
def resources(request):
	template = loader.get_template("pages/resources.html")
	context = RequestContext(request, {
		'exams' : ExamReview.objects.all(),
	})
	return HttpResponse(template.render(context))

def projects(request):
	template = "pages/projects.html"
	try:
		# Create anonymous (unauthenticated) GitHub session.
		anon = GitHub()
		# Fetch the "rit-csc" organization.
		ourOrg = anon.organization(login="rit-csc")
		# Iterate over all of our repositories and generate the dictionary
		# of info to be passed to the template.
		repos = {}
		for r in ourOrg.iter_repos(type='public'):
			# repos[str(r.name)] = {"description":r.description,"link_to_src":r.html_url}
			repos[r] = r.html_url
		if repos:
			return render_to_response(template, {"success":True, "repos":repos})
		else:
			return render_to_response(template, {"success":False, "goto":"http://github.com/rit-csc"})
	except GitHubError:
		pass
	finally:
		return render_to_response(template, {"success":False, "goto":"http://github.com/rit-csc"})
	
	