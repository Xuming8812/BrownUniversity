package edu.brown.cs.cs127.etl.importer;

import java.awt.List;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Time;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map.Entry;

import au.com.bytecode.opencsv.CSVReader;

public class EtlImporter
{
	/**
	 * You are only provided with a main method, but you may create as many
	 * new methods, other classes, etc as you want: just be sure that your
	 * application is runnable using the correct shell scripts.
	 */
	public static void main(String[] args) throws Exception
	{
		if (args.length != 4)
		{
			System.err.println("This application requires exactly four parameters: " +
					"the path to the airports CSV, the path to the airlines CSV, " +
					"the path to the flights CSV, and the full path where you would " +
					"like the new SQLite database to be written to.");
			System.exit(1);
		}

		//get parameters
		String AIRPORTS_FILE = args[0];
		String AIRLINES_FILE = args[1];
		String FLIGHTS_FILE = args[2];
		String DB_FILE = args[3];
		
		//connect to db
		Class.forName("org.sqlite.JDBC");
		Connection conn = DriverManager.getConnection("jdbc:sqlite:" + DB_FILE);
		
		Statement stat = conn.createStatement();
		stat.executeUpdate("PRAGMA foreign_keys = ON;");
		stat.executeUpdate("PRAGMA synchronous = OFF;");
		stat.executeUpdate("PRAGMA journal_mode = MEMORY;");
		stat.executeUpdate("DROP TABLE IF EXISTS flights;");
		stat.executeUpdate("DROP TABLE IF EXISTS airports;");
		stat.executeUpdate("DROP TABLE IF EXISTS airlines;");
		
		System.out.println("Connection Completed!");
		//create table for airports
		HashMap<String, Integer> airportsMap = createTableForAirports(conn, stat, AIRPORTS_FILE);		
		//create table for airlines
		HashMap<String, Integer> airlinesMap = createTableForAirlines(conn, stat,AIRLINES_FILE);
		//create table for flights
		HashMap<String, String[]>airportLocationMap = createTableForFlights(conn,stat,FLIGHTS_FILE,airportsMap,airlinesMap);	
		//fill the city and state info for airports
		updateTableAirports(conn, airportLocationMap);
		System.out.println("All done!");
		
		conn.close();
	}
	
	public static HashMap<String, String[]> createTableForFlights(Connection conn, 
											 Statement stat, 
											 String FLIGHTS_FILE,
											 HashMap<String, Integer> airportsMap,
											 HashMap<String, Integer> airlinesMap) throws Exception {
		//SQL command for creating table
		stat.executeUpdate("DROP TABLE IF EXISTS flights;");
		stat.executeUpdate("Create TABLE flights(\n" + 
				"  flight_id INTEGER PRIMARY KEY AUTOINCREMENT,\n" + 
				"  airline_id INTEGER NOT NULL,\n" + 
				"  flight_number INTEGER NOT NULL,\n" + 
				"  origin_airport INTEGER NOT NULL,\n" + 
				"  destination_airport INTEGER NOT NULL CHECK(destination_airport!=origin_airport),\n" + 
				"  departure_dt DATETIME,\n" + 
				"  departure_delay INTEGER,\n" + 
				"  arrival_dt DATETIME CHECK(arrival_dt>departure_dt),\n" + 
				"  arrival_delay INTEGER CHECK(strftime('%Y-%m-%d %H:%M', departure_dt, departure_delay || ' minute')<strftime('%Y-%m-%d %H:%M', arrival_dt, arrival_delay || ' minute')),\n" + 
				"  cancelled BOOLEAN,\n" + 
				"  carrier_delay INTEGER CHECK(carrier_delay>=0),\n" + 
				"  weather_delay INTEGER CHECK(weather_delay>=0),\n" + 
				"  air_traffic_delay INTEGER CHECK(air_traffic_delay>=0),\n" + 
				"  security_delay INTEGER CHECK(security_delay>=0),\n" + 
				"  CONSTRAINT airline_fk FOREIGN KEY(airline_id) REFERENCES airlines(airline_id),\n" + 
				"  CONSTRAINT origin_airport_fk FOREIGN KEY(origin_airport) REFERENCES airports(airport_id),\n" + 
				"  CONSTRAINT destination_airport_fk FOREIGN KEY(destination_airport) REFERENCES airports(airport_id)\n" +
				")");

		//SQL command for inserting values		
		PreparedStatement prep = conn.prepareStatement("INSERT OR IGNORE INTO flights (airline_id, "
				+ "flight_number,"
				+ "origin_airport,"
				+ "destination_airport,"
				+ "departure_dt,"
				+ "departure_delay,"
				+ "arrival_dt,"
				+ "arrival_delay,"
				+ "cancelled,"
				+ "carrier_delay,"
				+ "weather_delay,"
				+ "air_traffic_delay,"
				+ "security_delay)"
				+ "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");	
		//read in flight csv file
		CSVReader reader = new CSVReader(new FileReader(FLIGHTS_FILE));
		
		//begin to read in csv file
		String[] nextLine;
		
		HashMap<String, String[]> airportLocationMap = new HashMap<String, String[]>();
		
		while((nextLine = reader.readNext())!=null) {	
			//find airline_id
			String airlineCode = nextLine[0];
			if(airlinesMap.containsKey(airlineCode)) {
				prep.setInt(1, airlinesMap.get(airlineCode));
			}
			else {
				continue;
			}
			//get flight number
			prep.setInt(2, Integer.parseInt(nextLine[1]));	
			//get origin_airport
			String originAirportCode = nextLine[2];		
			if(airportsMap.containsKey(originAirportCode)) {
				prep.setInt(3, airportsMap.get(originAirportCode));
			} else {
				continue;
			}
			
			airportLocationMap.put(originAirportCode, new String[]{nextLine[3],nextLine[4]});
			
			//get destination_airport
			String destAirportCode = nextLine[5];			
			if(airportsMap.containsKey(destAirportCode)) {
				prep.setInt(4, airportsMap.get(destAirportCode));
			} else {
				continue;
			}
			airportLocationMap.put(destAirportCode, new String[]{nextLine[6],nextLine[7]});
			//get date and time of departure
			String dept_dt = parseDate(nextLine[8],nextLine[9]);
			if(dept_dt != null) {
				//System.out.println(dept_dt);
				prep.setString(5,dept_dt);
			} else {
				continue;
			}			
			//get diff time in minutes of departure
			prep.setInt(6, Integer.parseInt(nextLine[10]));
			//get data and time of arrival
			String arrival_dt = parseDate(nextLine[11],nextLine[12]);
			if(arrival_dt != null) {
				//System.out.println(arrival_dt);
				prep.setString(7,arrival_dt);		
			} else {
				continue;
			}	
			//get diff time in minutes of arrival
			prep.setInt(8, Integer.parseInt(nextLine[13]));			
			//get canceled
			prep.setString(9,(nextLine[14]));
			//get carrier_delay
			prep.setInt(10, Integer.parseInt(nextLine[15]));
			//get weather_delay
			prep.setInt(11, Integer.parseInt(nextLine[16]));
			//get air_traffic_delay
			prep.setInt(12, Integer.parseInt(nextLine[17]));
			//get security_delay
			prep.setInt(13, Integer.parseInt(nextLine[18]));	
			
			prep.addBatch();
		}	
			
		conn.setAutoCommit(false);
		prep.executeBatch();
		conn.setAutoCommit(true);
		
		reader.close();
			
		return airportLocationMap;		
	}
	
	public static HashMap<String, Integer> createTableForAirports(Connection conn, Statement stat, String AIRPORTS_FILE) throws Exception {
		stat.executeUpdate("DROP TABLE IF EXISTS airports;");
		stat.executeUpdate("CREATE TABLE airports (airport_id INTEGER PRIMARY KEY AUTOINCREMENT, "
				+ "airport_code CHAR(3) UNIQUE,"
				+ "airport_name TEXT,"
				+ "airport_city TEXT,"
				+ "airport_state TEXT); ");
		System.out.println("Table Creation Completed!");
		//read csv file and insert into the table airport
		PreparedStatement prep = conn.prepareStatement("INSERT OR IGNORE INTO airports (airport_code, "
				+ "airport_name, "
				+ "airport_city, "
				+ "airport_state) "
				+ "VALUES (?, ?, ?, ?)");
				
		//read in airport csv 
		CSVReader reader = new CSVReader(new FileReader(AIRPORTS_FILE));
		String[] nextLine;
		
		HashMap<String, Integer> airportsMap = new HashMap<>();
        		
		int airportIndex = 0;
		while((nextLine = reader.readNext()) != null) {	
			airportIndex++;
			prep.setString(1, nextLine[0]);
			prep.setString(2, nextLine[1]);
			prep.setString(3, "Null");
			prep.setString(4, "Null");
			prep.addBatch();
			airportsMap.put(nextLine[0], airportIndex);
		}
		
		conn.setAutoCommit(false);
		prep.executeBatch();
		conn.setAutoCommit(true);
		
		reader.close();
		
		System.out.println("Airports Completed!");
		
		return airportsMap;
	}
	
	public static HashMap<String, Integer> createTableForAirlines(Connection conn, Statement stat, String AIRLINES_FILE) throws Exception {
		stat.executeUpdate("DROP TABLE IF EXISTS airlines;");
		stat.executeUpdate("CREATE TABLE airlines (airline_id INTEGER PRIMARY KEY AUTOINCREMENT, "
				+ "airline_code CHAR(10) UNIQUE,"
				+ "airline_name TEXT); ");
		
		//read csv file and insert into the table airport
		PreparedStatement prep = conn.prepareStatement("INSERT OR IGNORE INTO airlines (airline_code, "
				+ "airline_name)"
				+ "VALUES (?, ?)");		

		CSVReader reader = new CSVReader(new FileReader(AIRLINES_FILE));
		HashMap<String, Integer> airlinesMap = new HashMap<>();
		int airlineIndex = 0;
		String[] nextLine;
		
		while((nextLine = reader.readNext()) != null) {	
			airlineIndex++;
			prep.setString(1, nextLine[0]);
			prep.setString(2, nextLine[1]);
			prep.addBatch();
			airlinesMap.put(nextLine[0], airlineIndex);
		}	
		
		conn.setAutoCommit(false);
		prep.executeBatch();
		conn.setAutoCommit(true);
		
		reader.close();	
		
		return airlinesMap;
	}
	
	public static void updateTableAirports(Connection conn, HashMap<String,String[]> airportLocationMap) throws Exception{				
		String updateCommand = "UPDATE airports SET airport_city=?, airport_state =? WHERE airport_code=?;";
		
		int index = 0;
		for(Entry<String, String[]> pair: airportLocationMap.entrySet()) {
			index++;
			
			PreparedStatement queryStatement = conn.prepareStatement(updateCommand);
			queryStatement.setString(1,pair.getValue()[0]);
			queryStatement.setString(2,pair.getValue()[1]);
			queryStatement.setString(3,pair.getKey());
			queryStatement.execute();	
		}
		
		System.out.println("Update done!");
	}
	
	public static int getAirlineId(String airlineCode, Connection conn) throws SQLException {
		String query = "SELECT airline_id from airlines where airline_code = ?;";
		
		PreparedStatement queryStatement = conn.prepareStatement(query);
		queryStatement.setString(1, airlineCode);
		ResultSet results = queryStatement.executeQuery();
		if(results.next()) {
			return Integer.parseInt(results.getString("airline_id"));
		}
		else {
			return -1;
		}
	}

	public static int getAirportId(String airportCode, Connection conn) throws SQLException {
		String query = "SELECT airport_id from airports where airport_code = ?;";
		
		PreparedStatement queryStatement = conn.prepareStatement(query);
		queryStatement.setString(1, airportCode);
		ResultSet results = queryStatement.executeQuery();
		if(results.next()) {
			return Integer.parseInt(results.getString("airport_id"));
		}
		else {
			return -1;
		}
	}

	public static String parseDate(String dateString, String timeString) {
		DateFormat standardDateFormat = new SimpleDateFormat("yyyy-MM-dd");
		DateFormat[] sampleDateFormats = {new SimpleDateFormat("MM-dd-yyyy"),
									  	  new SimpleDateFormat("MM/dd/yyyy"),																	  
									  	  new SimpleDateFormat("yyyy/MM/dd")};
		
		Date dateParsed = new Date();
		String date = null;
				
		try {
			standardDateFormat.setLenient(false);
			dateParsed = standardDateFormat.parse(dateString);
			date = standardDateFormat.format(dateParsed);
		} catch (ParseException e) {		
		}	
		
		for(int i = 0; i < 3; i++) {
			try {
				sampleDateFormats[i].setLenient(false);
				Date result = sampleDateFormats[i].parse(dateString);
				String sampleDateStringNormalized = standardDateFormat.format(result);
				dateParsed = standardDateFormat.parse(sampleDateStringNormalized);
				date = standardDateFormat.format(dateParsed);
				break;
			} catch (ParseException e) {		
			}			
		}
		
		DateFormat standardTimeFormat = new SimpleDateFormat("HH:mm");
		DateFormat sampleTimeFormat = new SimpleDateFormat("hh:mm a", Locale.US);
		sampleTimeFormat.setLenient(false);
		
		String time = null;
	
		try {
			//System.out.println(timeString);
			Date result = sampleTimeFormat.parse(timeString);
			time = standardTimeFormat.format(result);
			
		} catch (ParseException e) {
			time = timeString;
			
		}
		
		return date+" "+time;	
	}
	
}
