from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import User, Category, Base, Book

engine = create_engine('sqlite:///virtual_bookstore.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create user Catalog
User1 = User(name="User", email="user@yahoo.com",
             picture='https://goo.gl/images/343vyt')
session.add(User1)
session.commit()


# Fiction and Literature category
category1 = Category(user_id=1,
                     name="Fiction & Literature")

session.add(category1)
session.commit()


book1 = Book(user_id=1,
             name="a spark of light",
             picture="aSparkOfLight.jpg",
             author="Jodi Picoult",
             description="#1 NEW YORK TIMES BESTSELLER • The author of Small Great Things returns with a powerful and provocative new novel about ordinary lives that intersect during a heart-stopping crisis.",  # noqa E501
             category=category1)
session.add(book1)
session.commit()

book2 = Book(user_id=1,
             name="The Girl with the Dragon Tattoo",
             picture="theGirlWithTheDragonTattoo.jpg",
             author="Stieg Larsson",
             description="Murder mystery, family saga, love story, and financial intrigue combine into one satisfyingly complex and entertainingly atmospheric novel, the first in Stieg Larsson's thrilling Millenium series featuring Lisbeth Salander.",  # noqa E501
             category=category1)

session.add(book2)
session.commit()

book3 = Book(user_id=1,
             name="Hippie",
             picture="Hippie.jpg",
             author="Paulo Coelho",
             description="Drawing on the rich experience of his own life, best-selling author Paulo Coelho takes us back in time to relive the dreams of a generation that longed for peace and dared to challenge the established social order. In Hippie, he tells the story of Paulo, a young, skinny Brazilian man with a goatee and long, flowing hair, who wants to become a writer and sets off on a journey in search of a deeper meaning for his life.",  # noqa E501
             category=category1)

session.add(book3)
session.commit()

# Sci Fi & Fantasy Category
category2 = Category(user_id=1,
                     name="Sci-Fi & Fantasy")

session.add(category2)
session.commit()

book1 = Book(user_id=1,
             name="Harry Potter and the Goblet of Fire",
             picture="harryPotterAndTheGobletOfFire.jpg",
             author="J.K. Rowling",
             description="Harry Potter is midway through his training as a wizard and his coming of age. Harry wants to get away from the pernicious Dursleys and go to the International Quidditch Cup. He wants to find out about the mysterious event that's supposed to take place at Hogwarts this year, an event involving two other rival schools of magic, and a competition that hasn't happened for a hundred years. He wants to be a normal, fourteen-year-old wizard. But unfortunately for Harry Potter, he's not normal - even by wizarding standards. And in his case, different can be deadly.",  # noqa E501
             category=category2)
session.add(book1)
session.commit()

book2 = Book(user_id=1,
             name="The Lord of the Rings",
             picture="theLordOfTheRings.jpg",
             author="J.R.R. Tolkien",
             description="In ancient times the Rings of Power were crafted by the Elven-smiths, and Sauron, the Dark Lord, forged the One Ring, filling it with his own power so that he could rule all others. But the One Ring was taken from him, and though he sought it throughout Middle-earth, it remained lost to him. After many ages it fell by chance into the hands of the hobbit Bilbo Baggins.",  # noqa E501
             category=category2)

session.add(book2)
session.commit()

book3 = Book(user_id=1,
             name="Perelandra",
             picture="Perelandra.jpg",
             author="C.S. Lewis",
             description="The second book in C. S. Lewis's acclaimed Space Trilogy, which also includes Out of the Silent Planet and That Hideous Strength, Perelandra continues the adventures of the extraordinary Dr. Ransom. Pitted against the most destructive of human weaknesses, temptation, the great man must battle evil on a new planet -- Perelandra -- when it is invaded by a dark force. Will Perelandra succumb to this malevolent being, who strives to create a new world order and who must destroy an old and beautiful civilization to do so? Or will it throw off the yoke of corruption and achieve a spiritual perfection as yet unknown to man? The outcome of Dr. Ransom's mighty struggle alone will determine the fate of this peace-loving planet.",  # noqa E501
             category=category2)

session.add(book3)
session.commit()


# Mystery category
category3 = Category(user_id=1,
                     name="Mystery")

session.add(category3)
session.commit()

book1 = Book(user_id=1,
             name="The Neon Rain",
             picture="theNeonRain.jpg",
             author="James Lee Burke",
             description="New Orleans Detective Dave Robicheaux has fought too many battles: in Vietnam, with police brass, with killers and hustlers, and the bottle. Lost without his wife's love, Robicheaux haunts the intense and heady French Quarter—the place he calls home, and the place that nearly destroys him when he beomes involved in the case of a young prostitute whose body is found in a bayou. Thrust into the seedy world of drug lords and arms smugglers, Robicheaux must face down the criminal underworld and come to terms with his own bruised heart and demons to survive.",  # noqa E501
             category=category3)

session.add(book1)
session.commit()

book2 = Book(user_id=1,
             name="Magpie Murders",
             picture="magpieMurders.jpg",
             author="Anthony Horowitz",
             description="From the New York Times bestselling author of Moriarty and Trigger Mortis, this fiendishly brilliant, riveting thriller weaves a classic whodunit worthy of Agatha Christie into a chilling, ingeniously original modern-day mystery.",  # noqa E501
             category=category3)

session.add(book2)
session.commit()

book3 = Book(user_id=1,
             name="The Word is Murder: A Novel",
             picture="TheWordIsMurderANovel.jpg",
             description="New York Times bestselling author of Magpie Murders and Moriarty, Anthony Horowitz has yet again brilliantly reinvented the classic crime novel, this time writing a fictional version of himself as the Watson to a modern-day Holmes.",  # noqa E501
             author="Anthony Horowitz",
             category=category3)

session.add(book3)
session.commit()


# History Category
category4 = Category(user_id=1,
                     name="History")

session.add(category4)
session.commit()

book1 = Book(user_id=1,
             name="The History of the Ancient World",
             picture="TheHistoryoftheAncientWorld.jpg",
             description="A lively and engaging narrative history showing the common threads in the cultures that gave birth to our own.",  # noqa E501
             author="Susan Wise Bauer",
             category=category4)

session.add(book1)
session.commit()

book2 = Book(user_id=1,
             name="The History of the Medieval World",
             picture="theHistoryOfTheMedievalWorld.jpg",
             author="Susan Wise Bauer",
             description="A masterful narrative of the Middle Ages, when religion became a weapon for kings all over the world.",  # noqa E501
             category=category4)

session.add(book2)
session.commit()

book3 = Book(user_id=1,
             name="Rome's Last Citizen",
             picture="romesLastCitizen.jpg",
             author="Susan Wise Bauer",
             description="Rome's Last Citizen is a timeless story of an uncompromising man in a time of crisis and his lifelong battle to save the Republic.",  # noqa E501
             category=category4)

session.add(book3)
session.commit()


# Business Category
category5 = Category(user_id=1,
                     name="Business")

session.add(category5)
session.commit()

book1 = Book(user_id=1,
             name="Start Your Own Business",
             picture="startYourOwnBusiness.jpg",
             author="Entrepreneur Media, Inc.",
             description="Tapping into more than 33 years of small business expertise, the staff at Entrepreneur Media takes today’s entrepreneurs beyond opening their doors and through the first three years of ownership. This revised edition features amended chapters on choosing a business, adding partners, getting funded, and managing the business structure and employees, and also includes help understanding the latest tax and healthcare reform information and legalities.",  # noqa E501
             category=category5)

session.add(book1)
session.commit()

book2 = Book(user_id=1,
             name="The Business Book",
             picture="theBusinessBook.jpg",
             author="DK",
             description="The Business Book is the perfect primer to key theories of business and management, covering inspirational business ideas, business strategy and alternative business models. One hundred key quotations introduce you to the work of great commercial thinkers, leaders, and gurus from Henry Ford to Steve Jobs, and to topics spanning from start-ups to ethics.",  # noqa E501
             category=category5)

session.add(book2)
session.commit()

book3 = Book(user_id=1,
             name="Good To Great",
             picture="goodToGreat.jpg",
             author="Jim Collins",
             description="The Challenge: Built to Last, the defining management study of the nineties, showed how great companies triumph over time and how long-term sustained performance can be engineered into the DNA of an enterprise from the very beginning. But what about the company that is not born with great DNA? How can good companies, mediocre companies, even bad companies achieve enduring greatness?",  # noqa E501
             category=category5)

session.add(book3)
session.commit()

print("added books!")
