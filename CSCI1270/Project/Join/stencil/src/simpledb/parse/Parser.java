package simpledb.parse;

import java.util.*;
import simpledb.query.*;
import simpledb.record.Schema;

import simpledb.parse.*;

import static simpledb.parse.Lexer.*;

/**
 * The SimpleDB parser.
 * @author Edward Sciore
 */
public class Parser {
   private Lexer lex;
   private boolean selectAll = false;
   private List<String> emptyList;
   
   public Parser(String s) {
      lex = new Lexer(s);
   }
   
// Methods for parsing predicates, terms, expressions, constants, and fields
   
   public String field() {
      return lex.eatField();
   }
   
   public Constant constant() {
      if (lex.matchStringConstant())
         return new StringConstant(lex.eatStringConstant());
      else
         return new IntConstant(lex.eatIntConstant());
   }
   
   public Expression expression() {
      if (lex.matchId())
         return new FieldNameExpression(field());
      else
         return new ConstantExpression(constant());
   }
   
   public Term term() {
      Expression lhs = expression();
      lex.eatDelim('=');
      Expression rhs = expression();
      return new Term(lhs, rhs);
   }
   
   public Predicate predicate() {
      Predicate pred = new Predicate(term());
      if (lex.matchKeyword("and")) {
         lex.eatKeyword("and");
         pred.conjoinWith(predicate());
      }
      return pred;
   }
   
// Methods for parsing queries
   
   public QueryData query() {
      lex.eatKeyword("select");
      Collection<String> fields = selectList();
      lex.eatKeyword("from");
      Collection<String> tables = tableList();
      if (selectAll) {
         fields = addAllTableFields(tables);
      }
      Predicate pred = new Predicate();
      if (lex.matchKeyword("on")) {
         lex.eatKeyword("on");
         pred = predicate();
      }
      if (lex.matchKeyword("where")) {
         lex.eatKeyword("where");
         pred.conjoinWith(predicate());
      }
      return new QueryData(fields, tables, pred);
   }
   
   private Collection<String> selectList() {
      Collection<String> L = new ArrayList<String>();
      if (lex.matchDelim('*')) {
         lex.eatDelim('*');
         selectAll = true;
      } else {
         L.add(field());
      }
      if (lex.matchDelim(',')) {
         lex.eatDelim(',');
         L.addAll(selectList());
      }
      return L;
   }
   
   private Collection<String> tableList() {
      Collection<String> L = new ArrayList<String>();
      L.add(lex.eatId());
      if (lex.matchDelim(',')) {
         lex.eatDelim(',');
         L.addAll(tableList());
      } else if (lex.matchKeyword("join")) {
         lex.eatKeyword("join");
         L.addAll(tableList());
      } else if (lex.matchKeyword("inner")) {
         lex.eatKeyword("inner");
         if (lex.matchKeyword("join")) {
            lex.eatKeyword("join");
            L.addAll(tableList());
         } else {
            throw new BadSyntaxException();
         }
      }
      return L;
   }
   
// Methods for parsing the various update commands
   
   public Object updateCmd() {
      if (lex.matchKeyword("insert"))
         return insert();
      else if (lex.matchKeyword("delete"))
         return delete();
      else if (lex.matchKeyword("update"))
         return modify();
      else
         return create();
   }
   
   private Object create() {
      lex.eatKeyword("create");
      if (lex.matchKeyword("table"))
         return createTable();
      else if (lex.matchKeyword("view"))
         return createView();
      else
         return createIndex();
   }
   
// Method for parsing delete commands
   
   public DeleteData delete() {
      lex.eatKeyword("delete");
      lex.eatKeyword("from");
      String tblname = lex.eatId();
      Predicate pred = new Predicate();
      if (lex.matchKeyword("where")) {
         lex.eatKeyword("where");
         pred = predicate();
      }
      return new DeleteData(tblname, pred);
   }
   
// Methods for parsing insert commands
   
   public InsertData insert() {
      lex.eatKeyword("insert");
      lex.eatKeyword("into");
      String tblname = lex.eatId();
      lex.eatDelim('(');
      List<String> flds = fieldList();
      lex.eatDelim(')');
      lex.eatKeyword("values");
      lex.eatDelim('(');
      List<Constant> vals = constList();
      lex.eatDelim(')');
      return new InsertData(tblname, flds, vals);
   }
   
   private List<String> fieldList() {
      List<String> L = new ArrayList<String>();
      L.add(field());
      if (lex.matchDelim(',')) {
         lex.eatDelim(',');
         L.addAll(fieldList());
      }
      return L;
   }
   
   private List<Constant> constList() {
      List<Constant> L = new ArrayList<Constant>();
      L.add(constant());
      if (lex.matchDelim(',')) {
         lex.eatDelim(',');
         L.addAll(constList());
      }
      return L;
   }
   
// Method for parsing modify commands
   
   public ModifyData modify() {
      lex.eatKeyword("update");
      String tblname = lex.eatId();
      lex.eatKeyword("set");
      String fldname = field();
      lex.eatDelim('=');
      Expression newval = expression();
      Predicate pred = new Predicate();
      if (lex.matchKeyword("where")) {
         lex.eatKeyword("where");
         pred = predicate();
      }
      return new ModifyData(tblname, fldname, newval, pred);
   }
   
// Method for parsing create table commands
   
   public CreateTableData createTable() {
      lex.eatKeyword("table");
      String tblname = lex.eatId();
      lex.eatDelim('(');
      Schema sch = fieldDefs();
      lex.eatDelim(')');
      return new CreateTableData(tblname, sch);
   }
   
   private Schema fieldDefs() {
      Schema schema = fieldDef();
      if (lex.matchDelim(',')) {
         lex.eatDelim(',');
         Schema schema2 = fieldDefs();
         schema.addAll(schema2);
      }
      return schema;
   }
   
   private Schema fieldDef() {
      String fldname = field();
      return fieldType(fldname);
   }
   
   private Schema fieldType(String fldname) {
      Schema schema = new Schema();
      if (lex.matchKeyword("int")) {
         lex.eatKeyword("int");
         schema.addIntField(fldname);
      }
      else {
         lex.eatKeyword("varchar");
         lex.eatDelim('(');
         int strLen = lex.eatIntConstant();
         lex.eatDelim(')');
         schema.addStringField(fldname, strLen);
      }
      return schema;
   }
   
// Method for parsing create view commands
   
   public CreateViewData createView() {
      lex.eatKeyword("view");
      String viewname = lex.eatId();
      lex.eatKeyword("as");
      QueryData qd = query();
      return new CreateViewData(viewname, qd);
   }
   
   
//  Method for parsing create index commands
   
   public CreateIndexData createIndex() {
      lex.eatKeyword("index");
      String idxname = lex.eatId();
      lex.eatKeyword("on");
      String tblname = lex.eatId();
      lex.eatDelim('(');
      String fldname = field();
      lex.eatDelim(')');
      return new CreateIndexData(idxname, tblname, fldname);
   }

   /**
    * Adds all table fields if the '*' operator is used
    * @param tables input tables
    * @return list of fields
    */
   private Collection<String> addAllTableFields(Collection<String> tables) {
      List<String> fields = new ArrayList<>();
      for (String table : tables) {
         switch (table) {
            case "student":
               fields.addAll(STUDENT_FIELDS);
               break;
            case "dept":
               fields.addAll(DEPT_FIELDS);
               break;
            case "course":
               fields.addAll(COURSE_FIELDS);
               break;
            case "section":
               fields.addAll(SECTION_FIELDS);
               break;
            case "enroll":
               fields.addAll(ENROLL_FIELDS);
               break;
            case "business":
                fields.addAll(BUSINESS_FIELDS);
                break;
            case "review":
                fields.addAll(REVIEW_FIELDS);
                break;
            case "user":
                fields.addAll(USER_FIELDS);
                break;
            default:
               break;
         }
      }
      // Handle duplicate
      if (fields.contains("sid") && fields.contains("studentid")) {
         fields.remove("sid");
      }
      if (fields.contains("did") && fields.contains("deptid")) {
         fields.remove("did");
      }
      if (fields.contains("cid") && fields.contains("courseid")) {
         fields.remove("cid");
      }
      if (fields.contains("sectid") && fields.contains("sectionid")) {
         fields.remove("sectid");
      }
      return fields;
   }
}
