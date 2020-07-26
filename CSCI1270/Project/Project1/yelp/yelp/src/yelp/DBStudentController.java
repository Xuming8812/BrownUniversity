package yelp;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

/**
 * This is the class file you will have to modify. You should only have to modify this file
 * and nothing else.
 * 
 * You will have to connect to the yelp.db database given. Once you are connected to the database,
 * you can execute queries on that database. The result will be return in a ResultSet. Fill in the 
 * appropriate method for each query. 
 * 
 * @author 
 *
 */

/**
 * Below are some snippets of JDBC code that may prove useful
 * 
 * For more sample JDBC code, check out 
 * http://web.archive.org/web/20100814175321/http://www.zentus.com/sqlitejdbc/
 * 
 * ---
 * 
 *      // INITIALIZE THE CONNECTION
 *      Class.forName("org.sqlite.JDBC");
 *      Connection conn = DriverManager.getConnection("jdbc:sqlite:PATH_TO_DB_FILE");
 * ---
 * 
 * Using PreparedStatement:
 * 
 * public void someQuery(String businessID){
 * 		String query = "SELECT * from business WHERE id = ? ;";
 * 		PreparedStatement prep = conn.prepareStatement(query);
 * 		prep.setString(1, businessID);
 * 		ResultSet rs = prep.executeQuery();
 * 		while (rs.next()) {
 * 			System.out.println("id = " + rs.getString("id"));
 * 			System.out.println("name = " + rs.getString("name"));
 * 		}
 * 		rs.close();
 * }
 * 
 */

public class DBStudentController implements DBController {
	public Connection conn ;
	
	public DBStudentController() throws SQLException, ClassNotFoundException {
		// Initialize the connection.
		Class.forName("org.sqlite.JDBC");
		this.conn = DriverManager.getConnection(
				"jdbc:sqlite:/Users/mingxu/Brown/CSCI 1270/Project/Project1/yelp/yelp.db");
	}
	

	/**
	 * This function is called for query 1
	 * 
	 * Get the businesses in Providence, RI that are still open. 
	 * Results should be sorted by review counts in descending order. Return top 7 businesses.
	 * 
	 * @input N/A
	 * @output Six columns - the business id, name, full address, review count, photo url, and stars of the business.
	 * 
	 * @return A List of BusinessObject containing the result to the query.  
	 * @throws SQLException
	 */
	@Override
	public List<BusinessObject> query1() throws SQLException {
		// Your code goes here. Refer to BusinessObject.java
		// FOR FULL CREDIT make sure to set the id, name, address, reviewCount, photoUrl and stars properties of your BusinessObjects
		String query = "SELECT id,name,full_address,review_count,photo_url,stars "
				+ "FROM 'business' "
				+ "WHERE state='RI' AND city='Providence' AND open=1 "
				+ "ORDER BY review_count DESC LIMIT 7";
		
		PreparedStatement prep = conn.prepareStatement(query);
		
		ResultSet results = prep.executeQuery();
		
		List<BusinessObject> answer = new ArrayList<BusinessObject>();
		
		while(results.next()) {
			BusinessObject currentBusiness = new BusinessObject();
			
			currentBusiness.setId(results.getString("id"));
			currentBusiness.setName(results.getString("name"));
			currentBusiness.setAddress(results.getString("full_address"));
			currentBusiness.setPhotoUrl(results.getString("photo_url"));
			currentBusiness.setReviewCount(Integer.parseInt(results.getString("review_count")));
			currentBusiness.setStars(Double.parseDouble(results.getString("stars")));
			
			answer.add(currentBusiness);
		}
		
		return answer;
		
	}

	/**
	 * This function is called for query 2
	 * 
	 * Get the reviews for a particular business, given the business ID. 
	 * Results should be sorted by the review's useful vote counts in descending order. Return top 7 reviews.
	 * 
	 * @input businessID
	 * @output Four columns - the user id, name of the user, stars of the review, and text of the review.
	 * 
	 * 
	 * @return A List of ReviewObject containing the result to the query
	 * @throws SQLException
	 */
	@Override
	public List<ReviewObject> query2(String businessID) throws SQLException {
		// Your code goes here. Refer to ReviewObject.java
		// FOR FULL CREDIT make sure to set the id, name, stars, text properties of your ReviewObjects
		String query = "SELECT R.user_id, U.name, R.stars, R.text "
				+ "FROM 'review' as R, 'user' as U "
				+ "WHERE R.business_id = ? AND R.user_id = U.id "
				+ "ORDER By R.useful_votes LIMIT 7;";
		
		PreparedStatement prep = conn.prepareStatement(query);
		
		prep.setString(1, businessID);
		
		ResultSet results = prep.executeQuery();
		
		List<ReviewObject> answer = new ArrayList<ReviewObject>();
		
		while(results.next()) {
			ReviewObject currentReview = new ReviewObject();
			
			currentReview.setId(results.getString("user_id"));
			currentReview.setName(results.getString("name"));
			currentReview.setStars(Double.parseDouble(results.getString("stars")));
			currentReview.setText(results.getString("text"));
			
			answer.add(currentReview);
		}
		
		return answer;
	}

	/**
	 * This function is called for query 3
	 * 
	 * Find the average star rating across all reviews written by a particular user.
	 * 
	 * @input userID
	 * @output One columns - the average star rating.
	 * 
	 * @return the average star rating
	 * @throws SQLException
	 */
	@Override
	public double query3(String userID) throws SQLException {
		// Your code goes here.
		String query = "SELECT avg(stars) FROM 'review' WHERE user_id = ?;";
		
		PreparedStatement prep = conn.prepareStatement(query);
		
		prep.setString(1, userID);
		
		ResultSet results = prep.executeQuery();
		
		return Double.parseDouble(results.getString("avg(stars)"));
	}

	/**
	 * This function is called for query 4
	 * 
	 * Get the businesses in Providence, RI that have been reviewed by more than 5 'elite' users. 
	 * Users who have written more than 10 reviews are called 'elite' users. 
	 * Results should be ordered by the 'elite' user count in descending order. Return top 7 businesses.
	 * 
	 * @input N/A
	 * @output Seven columns - the business id, business name, business full address, review count, photo url, stars, and the count of the 'elite' users for the particular business.
	 * 
	 * @return A List of BusinessObject representing the results to the query.
	 * @throws SQLException
	 */
	@Override
	public List<BusinessObject> query4() throws SQLException {
		// Your code goes here. Refer to BusinessObject.java
		// FOR FULL CREDIT make sure to set the id, name, address, reviewCount, photoUrl, stars, and elite count properties of your BusinessObjects
		String query = "WITH elite AS (SELECT id from 'user' WHERE review_count>10),\n" + 
				"business_elite AS (SELECT business_id, COUNT(business_id) as elite_count FROM 'review' GROUP BY business_id HAVING user_id in elite),\n" + 
				"elite_RI AS (SELECT * from 'business', business_elite WHERE business.id = business_elite.business_id AND city = 'Providence' AND state='RI' AND elite_count>5)\n" + 
				"SELECT id, name, full_address, review_count, photo_url, stars, elite_count "
				+ "FROM elite_RI "
				+ "ORDER By elite_count DESC LIMIT 7;";
		
		PreparedStatement prep = conn.prepareStatement(query);
		
		ResultSet results = prep.executeQuery();
		
		List<BusinessObject> answer = new ArrayList<BusinessObject>();
		
		while(results.next()) {
			BusinessObject currentBusiness = new BusinessObject();
			
			currentBusiness.setId(results.getString("id"));
			currentBusiness.setName(results.getString("name"));
			currentBusiness.setAddress(results.getString("full_address"));
			currentBusiness.setPhotoUrl(results.getString("photo_url"));
			currentBusiness.setReviewCount(Integer.parseInt(results.getString("review_count")));
			currentBusiness.setStars(Double.parseDouble(results.getString("stars")));
			currentBusiness.setEliteCount(Integer.parseInt(results.getString("elite_count")));
			answer.add(currentBusiness);
		}
		
		return answer;		
	}

	/**
	 * This function is called for query 5
	 * 
	 * Get the businesses in Providence, RI that have the highest percentage of five star reviews, and have been reviewed at least 20 times.
	 * Results should be ordered by the percentage in descending order. Return top 7 businesses.
	 * 
	 * @input N/A
	 * @output Seven columns - the business id, business name, business full address, review count, photo url, stars, and percentage of five star reviews
	 * 
	 * @return A List of BusinessObject representing the results to the query.
	 * @throws SQLException
	 */
	@Override
	public List<BusinessObject> query5() throws SQLException {
		// Your code goes here. Refer to BusinessObject.java
		// FOR FULL CREDIT make sure to set the id, name, address, reviewCount, photoUrl, stars, and percentage properties of your BusinessObjects
		
		String query = "with five_star_count As (SELECT business_id, Cast (COUNT(*) as FLOAT) AS five_count FROM 'review' WHERE review.stars > 4 GROUP BY business_id),\n" + 
				"local_five_count AS (SELECT * From 'business',five_star_count WHERE business.id = five_star_count.business_id AND city='Providence' AND state='RI') \n" + 
				"SELECT id, name, full_address, review_count, five_count, photo_url, stars, five_count/review_count as percentage\n" + 
				"from local_five_count\n" + 
				"where review_count>20\n" + 
				"ORDER BY percentage DESC LIMIT 7;";
		
		PreparedStatement prep = conn.prepareStatement(query);
		
		ResultSet results = prep.executeQuery();
		
		List<BusinessObject> answer = new ArrayList<BusinessObject>();
		
		while(results.next()) {
			BusinessObject currentBusiness = new BusinessObject();
			
			currentBusiness.setId(results.getString("id"));
			currentBusiness.setName(results.getString("name"));
			currentBusiness.setAddress(results.getString("full_address"));
			currentBusiness.setPhotoUrl(results.getString("photo_url"));
			currentBusiness.setReviewCount(Integer.parseInt(results.getString("review_count")));
			currentBusiness.setStars(Double.parseDouble(results.getString("stars")));
			currentBusiness.setPercentage(Double.parseDouble(results.getString("percentage")));
			answer.add(currentBusiness);
		}
		
		return answer;
	}
}