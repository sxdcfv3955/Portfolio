package com.www.animal;

import java.text.DateFormat;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.Locale;

import javax.servlet.http.HttpServletRequest;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.ml.Pipeline;
import org.apache.spark.ml.PipelineModel;
import org.apache.spark.ml.PipelineStage;
import org.apache.spark.ml.classification.DecisionTreeClassifier;
import org.apache.spark.ml.feature.StringIndexer;
import org.apache.spark.ml.feature.VectorAssembler;
import org.apache.spark.sql.DataFrame;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.sql.SQLContext;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.StructField;
import org.apache.spark.sql.types.StructType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

/**
 * Handles requests for the application home page.
 */
@Controller
public class HomeController {
	static SparkConf conf = new SparkConf().setMaster("local[*]").setAppName("HomeController");
	static JavaSparkContext sc = new JavaSparkContext(conf);
	static SQLContext spark = new SQLContext(sc);

	StructField dt1 = DataTypes.createStructField("desertionNo", DataTypes.StringType, true);
	StructField dt2 = DataTypes.createStructField("state", DataTypes.StringType, true);
	StructField dt3 = DataTypes.createStructField("age", DataTypes.DoubleType, true);
	StructField dt4 = DataTypes.createStructField("weight", DataTypes.DoubleType, true);
	StructField dt5 = DataTypes.createStructField("weightCd", DataTypes.StringType, true);
	StructField dt6 = DataTypes.createStructField("ageN", DataTypes.DoubleType, true);
	StructField dt7 = DataTypes.createStructField("weightN", DataTypes.DoubleType, true);
	StructField dt9 = DataTypes.createStructField("kind", DataTypes.StringType, true);
	StructField dt10 = DataTypes.createStructField("neuterYn", DataTypes.StringType, true);
	StructField dt11 = DataTypes.createStructField("sexCd", DataTypes.StringType, true);
	StructField dt12 = DataTypes.createStructField("colorCd", DataTypes.StringType, true);
	StructField dt13 = DataTypes.createStructField("sgg", DataTypes.StringType, true);
	StructField dt16 = DataTypes.createStructField("weightS", DataTypes.IntegerType, true);
	StructField dt17 = DataTypes.createStructField("weightM", DataTypes.IntegerType, true);
	StructField dt18 = DataTypes.createStructField("sexF", DataTypes.IntegerType, true);
	StructField dt19 = DataTypes.createStructField("sexM", DataTypes.IntegerType, true);
	StructField dt20 = DataTypes.createStructField("neuterN", DataTypes.IntegerType, true);
	StructField dt21 = DataTypes.createStructField("sggGu", DataTypes.IntegerType, true);
	StructField dt22 = DataTypes.createStructField("sggSi", DataTypes.IntegerType, true);
	StructField dt23 = DataTypes.createStructField("stateX", DataTypes.IntegerType, true);
	StructField dt24 = DataTypes.createStructField("happenDt", DataTypes.StringType, true);
	StructField dt25 = DataTypes.createStructField("happenY", DataTypes.StringType, true);
	StructField dt26 = DataTypes.createStructField("happenM", DataTypes.StringType, true);
	StructField dt27 = DataTypes.createStructField("colohappenYM", DataTypes.StringType, true);
	StructField dt28 = DataTypes.createStructField("happenPlace", DataTypes.StringType, true);
	StructField dt29 = DataTypes.createStructField("careAddr", DataTypes.StringType, true);
	StructField dt30 = DataTypes.createStructField("careNm", DataTypes.StringType, true);
	StructField dt31 = DataTypes.createStructField("noticeSdt", DataTypes.StringType, true);
	StructField dt32 = DataTypes.createStructField("noticeEdt", DataTypes.StringType, true);
	StructField dt33 = DataTypes.createStructField("orgNm", DataTypes.StringType, true);
	StructField dt34 = DataTypes.createStructField("org", DataTypes.StringType, true);
	StructField dt35 = DataTypes.createStructField("specialMark", DataTypes.StringType, true);
	StructType schema = DataTypes.createStructType(
			Arrays.asList(dt1, dt2, dt3, dt4, dt5, dt6, dt7, dt9, dt10, dt11, dt12, dt13, dt16, dt17, dt18, dt19, dt20,
					dt21, dt22, dt23, dt24, dt25, dt26, dt27, dt28, dt29, dt30, dt31, dt32, dt33, dt34, dt35));

	DataFrame d0 = spark.read().format("com.databricks.spark.csv").option("header", "true").option("delimiter", ",")
			.option("inferSchema", "true").option("encoding", "UFT-8").schema(schema)
			.load("C:/Users/sxdcf/Desktop/Project/dog.csv");

	StringIndexer indexer = new StringIndexer().setInputCol("stateX").setOutputCol("label");

	VectorAssembler assembler = new VectorAssembler()
			.setInputCols(new String[] { "ageN", "weightN", "neuterN", "sggGu", "sggSi" }).setOutputCol("features");
	DataFrame df = assembler.transform(d0);

	DecisionTreeClassifier dt = new DecisionTreeClassifier().setLabelCol("label").setFeaturesCol("features");

	Pipeline pipeline_dt = new Pipeline().setStages(new PipelineStage[] { indexer, assembler, dt });
	PipelineModel model_dt = pipeline_dt.fit(d0);

	@RequestMapping(value = "/", method = RequestMethod.GET)
	public String home(Locale locale, Model model) throws Exception {
		System.out.println("home2");

		return "index";
	}

	@RequestMapping(value = "/index", method = RequestMethod.GET)
	public String index(Locale locale, Model model) {

		Date date = new Date();
		DateFormat dateFormat = DateFormat.getDateTimeInstance(DateFormat.LONG, DateFormat.LONG, locale);

		String formattedDate = dateFormat.format(date);

		model.addAttribute("serverTime", formattedDate);
		System.out.println("index");
		return "index";
	}

	@RequestMapping(value = "/services", method = RequestMethod.GET)
	public String services(HttpServletRequest httpServletRequest, Model model) {
		System.out.println("services");

		return "services";
	}
	
	@RequestMapping(value = "/services2", method = RequestMethod.GET)
	public String services2(HttpServletRequest httpServletRequest, Model model) {
		System.out.println("services2");

		return "services2";
	}

	@SuppressWarnings("finally")
	@RequestMapping(value = "/survival", method = RequestMethod.POST)
	public String survival(HttpServletRequest request, Model model) {
		try {
			String animalName = request.getParameter("animal_name");
			String age = request.getParameter("age");
			String weight = request.getParameter("weight");
			String selectNeuter = request.getParameter("select_neuter");
			String selectSgg = request.getParameter("select_sgg");
			int neuterN = 0;
			int sggGu = 0;
			int sggSi = 0;
			String str = "";

			System.out.println(animalName);
			model.addAttribute("live", animalName);

			double ageN = (Double.parseDouble(age)) / 19;
			double weightN = (Double.parseDouble(weight)) / 85;

			if (selectNeuter.equals("neuterY")) {
				neuterN = 1;
			} else
				neuterN = 0;

			if (selectSgg.contains("시")) {
				sggGu = 0;
				sggSi = 1;
			} else if (selectSgg.contains("군")) {
				sggGu = 0;
				sggSi = 0;
			} else if (selectSgg.contains("구")) {
				sggGu = 1;
				sggSi = 0;
			} else {
				str = "주소가 잘못 입력되었습니다.";
				model.addAttribute("bye", str);
				return "survival";

			}

			DTO animal_info = new DTO(ageN, weightN, neuterN, sggGu, sggSi);

			List<DTO> list = Arrays.asList(animal_info);
			DataFrame df = spark.createDataFrame(list, DTO.class);
			df.printSchema();
			df.show();

			DataFrame live = model_dt.transform(df);
			live.show();

			if (live.select("prediction").collectAsList().get(0).getDouble(0) == 1) {
				System.out.println("입양될 확률이 높습니다! 🎉");
				str = "입양될 확률이 높습니다! 🎉";
				model.addAttribute("bye", str);
			} else {
				System.out.println("입양될 확률이 낮습니다 ㅠ_ㅠ 😢");
				str = "입양될 확률이 낮습니다 ㅠ_ㅠ 😢";
				model.addAttribute("bye", str);
			}

//        return "survival";
		} catch (Exception e) {
			String str = "입력하지 않은 정보가 있어요!";
			model.addAttribute("bye", str);
		} finally {
			return "survival";
		}

	}

	@RequestMapping(value = "/about", method = RequestMethod.GET)
	public String about(Locale locale, Model model) {
		System.out.println("about");

		return "about";
	}

	@RequestMapping(value = "/shelter", method = RequestMethod.GET)
	public String selter(Locale locale, Model model) {
		System.out.println("shelter");

		return "shelter";
	}
	
	@RequestMapping(value = "/shelter2", method = RequestMethod.GET)
	public String selter2(Locale locale, Model model) {
		System.out.println("shelter2");

		return "shelter2";
	}

}