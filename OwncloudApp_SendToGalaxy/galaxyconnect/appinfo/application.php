<?php
/**
 * ownCloud - galaxyconnect
 *
 */

namespace OCA\Galaxyconnect\AppInfo;


use \OCP\AppFramework\App;

use \OCA\Galaxyconnect\Controller\PageController;


class Application extends App {


	public function __construct (array $urlParams=array()) {
		parent::__construct('convert', $urlParams);

		$container = $this->getContainer();

		/**
		 * Controllers
		 */
		$container->registerService('PageController', function($c) {
			return new PageController(
				$c->query('AppName'), 
				$c->query('Request'),
				$c->query('UserId')
			);
		});


		/**
		 * Core
		 */
		$container->registerService('UserId', function($c) {
			return \OCP\User::getUser();
		});		
		
	}


}
