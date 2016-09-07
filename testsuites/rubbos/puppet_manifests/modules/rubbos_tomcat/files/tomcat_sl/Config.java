package edu.rice.rubbos.servlets;


public class Config
{

  /**
   * Creates a new <code>Config</code> instance.
   */
  Config()
  {
  }


  public static final String HTMLFilesPath                 = "REPLACED_RUBBOS_HOME/Servlet_HTML";
  public static final String DatabaseProperties            = "REPLACED_RUBBOS_HOME/Servlets/mysql.properties";
  public static final int DatabasePropertiesSize = 1;

  public static final int    AboutMePoolSize               = 10;
  public static final int    BrowseCategoriesPoolSize      = 6;
  public static final int    BrowseRegionsPoolSize         = 6;
  public static final int    BuyNowPoolSize                = 4;
  public static final int    PutBidPoolSize                = 8;
  public static final int    PutCommentPoolSize            = 2;
  public static final int    RegisterItemPoolSize          = 2;
  public static final int    RegisterUserPoolSize          = 2;
  public static final int    SearchItemsByCategoryPoolSize = 15;
  public static final int    SearchItemsByRegionPoolSize   = 20;
  public static final int    StoreBidPoolSize              = 8;
  public static final int    StoreBuyNowPoolSize           = 4;
  public static final int    StoreCommentPoolSize          = 2;
  public static final int    ViewBidHistoryPoolSize        = 4;
  public static final int    ViewItemPoolSize              = 20;
  public static final int    ViewUserInfoPoolSize          = 4;
}
