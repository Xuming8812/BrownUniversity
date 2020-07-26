package edu.brown.cs.cs127.etl.query;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class EtlQuery
{
	private Connection conn;

	public EtlQuery(String pathToDatabase) throws Exception
	{
		Class.forName("org.sqlite.JDBC");
		conn = DriverManager.getConnection("jdbc:sqlite:" + pathToDatabase);

		Statement stat = conn.createStatement();
		stat.executeUpdate("PRAGMA foreign_keys = ON;");
	}

	public ResultSet query1(String[] args) throws SQLException
	{
		PreparedStatement stat = conn.prepareStatement(
			"SELECT COUNT(airport_code) AS airport_count FROM airports"
		);
		return stat.executeQuery();
	}

	public ResultSet query2(String[] args) throws SQLException
	{
		PreparedStatement stat = conn.prepareStatement(
			"SELECT COUNT(airline_code) AS airline_count FROM airlines"
		);
		return stat.executeQuery();
	}
	
	public ResultSet query3(String[] args) throws SQLException
	{
		PreparedStatement stat = conn.prepareStatement(
			"SELECT COUNT(flight_id) AS flight_count FROM flights"
		);
		return stat.executeQuery();
	}
	
	public ResultSet query4(String[] args) throws SQLException
	{
		PreparedStatement stat = conn.prepareStatement(
			"SELECT * FROM (\n" + 
			"	SELECT 'Air Traffic Delay' AS delay_reason, COUNT(*) AS delay FROM flights WHERE air_traffic_delay>0 UNION\n" + 
			"	SELECT 'Carrier Delay', COUNT(*) FROM flights WHERE carrier_delay>0 UNION\n" + 
			"	SELECT 'Weather Delay', COUNT(*) FROM flights WHERE weather_delay>0 UNION\n" + 
			"	SELECT 'Security Delay', COUNT(*) FROM flights WHERE security_delay>0\n" + 
			") ORDER BY delay DESC"
		);
		return stat.executeQuery();
	}
	
	public ResultSet query5(String[] args) throws SQLException
	{
		String dateInput = args[0] + "/" + args[1] + "/" + args[2];
		String date = normalizeDate(dateInput);
		
		PreparedStatement stat = conn.prepareStatement(
			"WITH flightsOnDate AS(\n" + 
			"	SELECT flight_id,airline_id,date(departure_dt) AS departure_date FROM flights WHERE departure_date = ?)\n" + 
			"SELECT airline_name, COUNT(flight_id) AS flight_count \n" + 
			"FROM airlines LEFT JOIN flightsOnDate ON flightsOnDate.airline_id = airlines.airline_id\n" + 
			"GROUP by airline_name ORDER BY flight_count DESC, airline_name;"
		);
		stat.setString(1, date);
		return stat.executeQuery();
	}
	
	public ResultSet query6(String[] args) throws SQLException
	{
		String dateInput = args[0] + "/" + args[1] + "/" + args[2];
		String date = normalizeDate(dateInput);
		
		String query = 
			"WITH arrivalOnDate AS (\n" + 
			"      SELECT destination_airport, flight_id FROM flights WHERE Date(arrival_dt) = ?),\n" + 
			"     deptOnDate AS (\n" + 
			"      SELECT origin_airport, flight_id FROM flights WHERE Date(departure_dt) = ?),\n" + 
			"     airportDept AS (\n" + 
			"       Select airport_name, COUNT(flight_id) AS number_dept \n" + 
			"       FROM airports left JOIN deptOnDate ON deptOnDate.origin_airport=airports.airport_id GROUP BY airports.airport_id),\n" + 
			"     airportArrival AS (\n" + 
			"       Select airport_name, COUNT(flight_id) AS number_arrival \n" + 
			"       FROM airports left JOIN arrivalOnDate ON arrivalOnDate.destination_airport=airports.airport_id GROUP BY airports.airport_id)\n" + 
			"SELECT airport_name, number_dept, number_arrival FROM airportDept NATURAL JOIN airportArrival WHERE airport_name=?";
		
		for (int i = 4; i < args.length; i++) {
			query += "OR airport_name = ? ";
		}
		
		query += "ORDER BY airport_name";
		
		PreparedStatement stat = conn.prepareStatement(query);
				
		stat.setString(1, date);
		stat.setString(2, date);
		for (int i = 3; i < args.length; i++) 
			stat.setString(i, args[i]);
		
		return stat.executeQuery();
	}

	public ResultSet query7(String[] args) throws SQLException
	{
		PreparedStatement stat = conn.prepareStatement(
			"WITH departureSchedule AS (\n" + 
			"		SELECT airline_name, flight_number, cancelled, departure_delay, arrival_delay\n" + 
			"		FROM flights JOIN airlines ON flights.airline_id = airlines.airline_id\n" + 
			"		WHERE airline_name = ? AND flight_number = ? AND DATE(departure_dt) BETWEEN ? AND ?), \n" + 
			"	totalCount AS (SELECT COUNT(*) AS number_schedule FROM departureSchedule), \n" + 
			"	cancelCount AS (SELECT COUNT(*) AS number_cancel FROM departureSchedule WHERE cancelled = 1), \n" + 
			"	departEarly AS (SELECT COUNT(*) AS number_early_depart FROM departureSchedule WHERE cancelled = 0 AND departure_delay <= 0), \n" + 
			"	departLate AS (SELECT COUNT(*) AS number_late_depart FROM departureSchedule WHERE cancelled = 0 AND departure_delay > 0), \n" + 
			"	arriveEarly AS (SELECT COUNT(*) AS number_early_arrive FROM departureSchedule WHERE cancelled = 0 AND arrival_delay <= 0), \n" + 
			"	arriveLate AS (SELECT COUNT(*) AS number_late_arrive FROM departureSchedule WHERE cancelled = 0 AND arrival_delay > 0) \n" + 
			"SELECT * FROM totalCount, cancelCount, departEarly, departLate, arriveEarly, arriveLate;"
		);
				
		stat.setString(1, args[0]);
		stat.setString(2, args[1]);
		stat.setString(3, normalizeDate(args[2]));
		stat.setString(4, normalizeDate(args[3]));
		
		return stat.executeQuery();
	}
	
	public ResultSet query8(String[] args) throws SQLException
	{
		PreparedStatement stat = conn.prepareStatement(
			"WITH deptAirport AS(SELECT airport_id,airport_code AS dept_code FROM airports WHERE airport_city=? AND airport_state=?),\n" + 
			"arrivalAirport AS(SELECT airport_id,airport_code AS arrival_code FROM airports WHERE airport_city=? AND airport_state=?),\n" + 
			"flightsSelected AS(SELECT airline_code, flight_number, dept_code, strftime('%Y-%m-%d %H:%M', departure_dt, departure_delay || ' minute') as deptTime,\n" + 
			"                  arrival_code, strftime('%Y-%m-%d %H:%M', arrival_dt, arrival_delay || ' minute') as arrivalTime \n" + 
			"                  FROM flights JOIN airlines ON airlines.airline_id = flights.airline_id \n" + 
			"                  JOIN deptAirport ON deptAirport.airport_id = flights.origin_airport \n" + 
			"                  JOIN arrivalAirport ON arrivalAirport.airport_id = flights.destination_airport\n" + 
			"                  WHERE cancelled = 0 AND DAte(deptTime) = ? AND date(arrivalTime)=?)\n" + 
			"Select airline_code, flight_number, dept_code AS origin_airport, strftime('%H:%M', deptTime) As departure_time, \n" + 
			"arrival_code AS destination_airport, strftime('%H:%M', arrivalTime) As arrival_time,\n" + 
			"(strftime('%H',arrivalTime) - strftime('%H',deptTime))*60 + strftime('%M',arrivalTime) - strftime('%M',deptTime) as duration_minutes\n" + 
			"from flightsSelected ORDER BY duration_minutes, airline_code;"
		);
			
		stat.setString(1, args[0]);
		stat.setString(2, args[1]);
		stat.setString(3, args[2]);
		stat.setString(4, args[3]);
		stat.setString(5, normalizeDate(args[4]));
		stat.setString(6, normalizeDate(args[4]));
		
		return stat.executeQuery();
	}
	
	public ResultSet query9(String[] args) throws SQLException
	{
		PreparedStatement stat = conn.prepareStatement(
			"WITH flightsSelected AS (\n" + 
			"  SELECT flight_id, airline_code, flight_number, a1.airport_code AS dept_code, a1.airport_city AS dept_city, a1.airport_state AS dept_state,\n" + 
			"  strftime('%Y-%m-%d %H:%M', departure_dt, departure_delay || ' minute') AS deptTime, \n" + 
			"  a2.airport_code AS arrival_code, a2.airport_city AS arrival_city, a2.airport_state AS arrival_state,\n" + 
			"  strftime('%Y-%m-%d %H:%M', arrival_dt, arrival_delay || ' minute') AS arrivalTime \n" + 
			"  FROM flights JOIN airlines ON airlines.airline_id = flights.airline_id \n" + 
			"  JOIN airports AS a1 ON a1.airport_id = flights.origin_airport \n" + 
			"  JOIN airports AS a2 ON a2.airport_id = flights.destination_airport \n" + 
			"  WHERE cancelled = 0 AND DATE(deptTime) = ? AND DATE(arrivalTime) = ?) \n" + 
			"SELECT f1.airline_code AS airline_code1, f1.flight_number AS flight_number1, f1.dept_code AS origin_airport1, \n" + 
			"strftime('%H:%M', f1.deptTime) AS departure_time1, f1.arrival_code AS destination_airport1, strftime('%H:%M', f1.arrivalTime) AS arrival_time1, \n" + 
			"f2.airline_code as airline_code2, f2.flight_number As flight_number2, f2.dept_code AS origin_airport2, \n" + 
			"strftime('%H:%M', f2.deptTime) AS departure_time2, f2.arrival_code AS destination_airport2, strftime('%H:%M', f2.arrivalTime) AS arrival_time2, \n" + 
			"(strftime('%H',f2.arrivalTime) - strftime('%H',f1.deptTime))*60 + strftime('%M',f2.arrivalTime) - strftime('%M',f1.deptTime) AS duration_minutes \n" + 
			"FROM flightsSelected AS f1 JOIN flightsSelected AS f2 ON f1.arrival_code = f2.dept_code \n" + 
			"WHERE f1.dept_city = ? AND f1.dept_state = ? AND (f2.dept_city != f1.dept_city OR f2.dept_state != f1.dept_state) AND\n" + 
			"(f1.arrival_city !=  f2.arrival_city OR f1.arrival_state !=  f2.arrival_state) AND f2.arrival_city = ? AND f2.arrival_state = ? AND\n" + 
			"f1.arrivalTime < f2.deptTime\n" + 
			"ORDER by duration_minutes, airline_code1, airline_code2, departure_time1"
		);
				
		stat.setString(1, normalizeDate(args[4]));
		stat.setString(2, normalizeDate(args[4]));
		stat.setString(3, args[0]);
		stat.setString(4, args[1]);
		stat.setString(5, args[2]);
		stat.setString(6, args[3]);
			
		return stat.executeQuery();
	}
	
	
	public ResultSet query10(String[] args) throws SQLException
	{
		PreparedStatement stat = conn.prepareStatement(
			"WITH flightsSelected AS (\n" + 
			"  SELECT flight_id, airline_code, flight_number, a1.airport_code AS dept_code, a1.airport_city AS dept_city, a1.airport_state AS dept_state,\n" + 
			"  strftime('%Y-%m-%d %H:%M', departure_dt, departure_delay || ' minute') AS deptTime, \n" + 
			"  a2.airport_code AS arrival_code, a2.airport_city AS arrival_city, a2.airport_state AS arrival_state,\n" + 
			"  strftime('%Y-%m-%d %H:%M', arrival_dt, arrival_delay || ' minute') AS arrivalTime \n" + 
			"  FROM flights JOIN airlines ON airlines.airline_id = flights.airline_id \n" + 
			"  JOIN airports AS a1 ON a1.airport_id = flights.origin_airport \n" + 
			"  JOIN airports AS a2 ON a2.airport_id = flights.destination_airport \n" + 
			"  WHERE cancelled = 0 AND DATE(deptTime) = ? AND DATE(arrivalTime) = ?) \n" + 
			"SELECT f1.airline_code AS airline_code1, f1.flight_number AS flight_number1, f1.dept_code AS origin_airport1, \n" + 
			"strftime('%H:%M', f1.deptTime) AS departure_time1, f1.arrival_code AS destination_airport1, strftime('%H:%M', f1.arrivalTime) AS arrival_time1, \n" + 
			"f2.airline_code as airline_code2, f2.flight_number As flight_number2, f2.dept_code AS origin_airport2, \n" + 
			"strftime('%H:%M', f2.deptTime) AS departure_time2, f2.arrival_code AS destination_airport2, strftime('%H:%M', f2.arrivalTime) AS arrival_time2, \n" + 
			"f3.airline_code AS airline_code3, f3.flight_number AS flight_number3, f3.dept_code AS origin_airport3, \n" + 
			"strftime('%H:%M', f3.deptTime) AS departure_time3, f3.arrival_code AS destination_airport3, strftime('%H:%M', f3.arrivalTime) AS arrival_time3, \n" + 
			"(strftime('%H',f3.arrivalTime) - strftime('%H',f1.deptTime))*60 + strftime('%M',f3.arrivalTime) - strftime('%M',f1.deptTime) AS duration_minutes \n" + 
			"FROM flightsSelected AS f1 JOIN flightsSelected AS f2 ON f1.arrival_code = f2.dept_code \n" + 
			"JOIN flightsSelected AS f3 ON f2.arrival_code = f3.dept_code\n" + 
			"WHERE f1.dept_city = ? AND f1.dept_state = ? AND (f1.arrival_city != f3.arrival_city OR f1.arrival_state != f3.arrival_state) \n" + 
			"AND (f3.dept_city != f1.dept_city OR f3.dept_state != f1.dept_state) AND f3.arrival_city = ? AND f3.arrival_state = ? AND\n" + 
			"f1.arrivalTime < f2.deptTime AND f2.arrivalTime < f3.deptTime\n" + 
			"ORDER by duration_minutes, airline_code1, airline_code2, airline_code3, departure_time1"
		);
					
		stat.setString(1, normalizeDate(args[4]));
		stat.setString(2, normalizeDate(args[4]));
		stat.setString(3, args[0]);
		stat.setString(4, args[1]);
		stat.setString(5, args[2]);
		stat.setString(6, args[3]);
				
		return stat.executeQuery();
	}
	
	
	private String normalizeDate(String date) {
		DateFormat standardFormat = new SimpleDateFormat("yyyy-MM-dd");
        DateFormat sampleFormat = new SimpleDateFormat("MM/dd/yyyy");
        Date parsedDate = null;
        
        try {
        	sampleFormat.setLenient(false);
            parsedDate = sampleFormat.parse(date);
            return standardFormat.format(parsedDate);
        }
        catch (ParseException e) {
        	return null;
        }
	}	
}
