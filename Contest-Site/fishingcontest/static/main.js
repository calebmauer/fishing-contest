/* 	Main Javascript code for fishing-contest. License: GPL v3 
	Requires angular and jQuery.
*/

$(document).ready(function() {
    $('#first-name').focus();
	$("#year").text((new Date()).getFullYear());
});

function ContestantService($http) {
	this.getContestants = function(callback) {
		$http.get("contestantlist/").success(function(data){
			callback(data.contestants);
		});
	};
	
	this.addContestant = function(first,last,age,gender,callback) {
		$http.get("addcontestant/",
		{params: {firstName: first, lastName: last, age: age, gender: gender}})
		.success(function(data){
			callback(data);
		});
	};
	
	this.deleteContestant = function(contestantid,callback) {
		$http.get("deletecontestant/", {params: {contestantid: contestantid}}).success(function(data){
			callback(data);
		});
	};
	
	this.getFish = function(contestantid,callback) {
		$http.get("fishlist/",{params:{contestantid:contestantid}}).success(function(data){
			callback(data);
		});
	};
	
	this.addFish = function(contestantid,weight,callback) {
		$http.get("addfish/",{params:{contestantid:contestantid,weight:weight}}).success(function(data){
			callback(data);
		});
	};
	
	this.deleteFish = function(fishid,callback) {
		$http.get("deletefish/",{params:{fishid:fishid}}).then(function(data){
			callback(data);
		});
	};
}

function Contestants($scope,ContestantService) {
	
	// True when the lists of contestants has loaded from get request
	this.loaded = false;
	
	// Setup new contestant fields
	this.new_contestant = {firstName:"",lastName:"",age:"",gender:"M",}

	this.loadContestants = function() {
		ContestantService.getContestants(function (contestants) {
			$.each(contestants, function(id,contestant) {
				contestant.show_fish=false;
				contestant.fish = {};
				contestant.fishCount = 0;
				contestant.new_fish = {weight:""};
			}.bind(this));
			this.items = contestants;
			this.loaded = true;
		}.bind(this));
	}.bind(this);
	
	this.loadContestants();
	
	this.contestantClick = function(contestantid) {
		contestant = this.items[contestantid];
		contestant.show_fish = !contestant.show_fish;

		// If fish already loaded, remove it. Toggle functionality.
		if (contestant.show_fish) {
			ContestantService.getFish(contestantid,function(fish) {
				contestant.fish = fish;
				contestant.fishCount = Object.keys(contestant.fish).length;
				$('#c_'+contestantid).find(".new-weight").focus();
			}.bind(this));
		} else {
			contestant.fish = {};
			contestant.fishCount = 0;
		}
	}.bind(this);
	
	this.addContestant = function() {
		
		newContestant = this.new_contestant;
		
		ContestantService.addContestant(newContestant.firstName, newContestant.lastName, newContestant.age, newContestant.gender,
		function(contestant) {
			this.items[contestant.id] = contestant;
			newContestant.firstName = '';
			newContestant.lastName = '';
			newContestant.gender = 'M';
			newContestant.age = '';
			$('#first-name').focus();
		}.bind(this));
	}.bind(this);
	
	this.count = function() {
		return (this.items) ? Object.keys(this.items).length : 0;
	}
	
	this.addFish = function(contestantid) {
		contestant = this.items[contestantid]
		new_weight = this.items[contestantid].new_fish.weight;
		
		// Add a new fish to this contestant and insert the new fish into contestant's list
		ContestantService.addFish(contestantid,new_weight,function(newFish){
			contestant.fish[newFish.id] = newFish;
			contestant.new_fish.weight = "";
			contestant.fishCount += 1;
		}.bind(this));
	}
}

function contestantContext(ContestantService) {
    // Adds a context menu to contestant list items
	return function(scope,element,attrs) {
		element.contextMenu({
			menu: 'deleteMenu'
		},
			function(action, el, pos) {
				if (action == "refresh") {
					location.reload();
				} else if (action == "delete") {
					ContestantService.deleteContestant(scope.contestant.id, function(data) {
						delete scope.contestants.items[scope.contestant.id];
					});
				}
			}
		);
	}
}

function fishContext(ContestantService) {
    // Adds a context menu to fish list items
	return function(scope,element,attrs){

		element.contextMenu({
			menu: 'deleteFishMenu'
		},
			function(action, el, pos) {
				if (action == "refreshfish") {
					location.reload();
				} else if (action == "deletefish") {
					ContestantService.deleteFish(scope.fish.id, function() {
						delete scope.contestant.fish[scope.fish.id];
						scope.contestant.fishCount += 1;
					});
				}
		});
	}
}

function focusWeightBox() {
    // Focus the weight entry box after the contestant's
	// fish collection changes
	return function(scope,element,attrs){
		scope.$watch('contestant.fishCount', function() {
			element.focus();
		});	
	};
}

angular
  .module('app',[])
  .service('ContestantService', ContestantService);
angular
  .module('app')
  .controller('Contestants', Contestants);
angular
  .module('app')
  .directive('contestantContext', contestantContext)
  .directive('fishContext', fishContext)
  .directive('focusWeightBox',focusWeightBox);